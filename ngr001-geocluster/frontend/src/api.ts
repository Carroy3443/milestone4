/**
 * API Client Module
 * 
 * This module provides functions for communicating with the NGR001 Geospatial API.
 * It handles HTTP requests for fetching events, updating events, and retrieving
 * H3 hexagonal aggregations.
 * 
 * @module api
 */

import { API_BASE } from "./config"
import {hexToBox} from "./utils/h3"

/** Base URL for the API, configured via environment variable or defaults to localhost */
export const API = API_BASE;

/**
 * Fetch all events within a specific H3 hexagon.
 * 
 * Converts the H3 index to a bounding box and queries the API for all events
 * within that geographic area.
 * 
 * @param h3 - H3 hexagon index string
 * @returns Promise resolving to an array of event objects, or empty array on error
 */
export async function fetchEventsInHex(h3: string) {
  //Get the parameters for the API call
  const {minx, miny, maxx, maxy} = hexToBox(h3);
  const qs = new URLSearchParams({
    minx: String(minx),
    miny: String(miny),
    maxx: String(maxx),
    maxy: String(maxy),
    limit: "10000"
  });

  //Get the url from the parameters
  const url = `${API}/events?${qs.toString()}`;
  
  //Fetch
  try {
    const r = await fetch(url, { headers: { Accept: "application/json" } });
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (e) {
    console.error("fetchEventsInHex failed:", url, e);
    return [];
  }
}

/**
 * Update multiple events in bulk via the API.
 * 
 * Sends a PATCH request to update event properties for multiple events
 * in a single transaction.
 * 
 * @param events - Array of event objects with id and fields to update
 * @returns Promise resolving to the API response
 * @throws Error if the HTTP request fails
 */
export async function updateEventsBulk(events: any[]){
  try {
    const r = await fetch(`${API}/events/bulk_update`, {
      method: "PATCH",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(events)
    })
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch (e) {
    console.error("updateEventsBulk failed:", e);
    throw e;
  }
}

/**
 * Fetch H3 hexagonal aggregations from the API.
 * 
 * Queries the API for event counts aggregated into H3 hexagonal bins
 * within the specified viewport and parameters.
 * 
 * @param params - Query parameters including:
 *   - minx, miny, maxx, maxy: Bounding box coordinates
 *   - res: H3 resolution level (5-9)
 *   - include: Array of dataset IDs to include
 *   - sources: Comma-separated dataset IDs (alternative to include)
 * @returns Promise resolving to array of {h3: string, count: number} objects
 */
export async function fetchH3(params: Record<string, string | number | string[]>) {
  const qs = new URLSearchParams();
  let sourcesComma = "";

  for (const [k, v] of Object.entries(params)) {
    if (Array.isArray(v)) {
      v.forEach((val) => qs.append(k, String(val))); // include=a&include=b...
      if (k === "include") sourcesComma = v.join(",");
    } else if (v !== undefined && v !== null) {
      qs.set(k, String(v));
      if (k === "sources") sourcesComma = String(v);
    }
  }
  if (sourcesComma && !qs.has("sources")) qs.set("sources", sourcesComma);

  const url = `${API}/aggregations/h3?${qs.toString()}`;
  try {
    const r = await fetch(url, { headers: { Accept: "application/json" } });
    if (!r.ok) throw new Error(`HTTP ${r.status} ${r.statusText}`);
    const json = await r.json();
    if (!Array.isArray(json)) throw new Error("Expected array JSON");
    return json as Array<{ h3: string; count: number }>;
  } catch (e) {
    console.error("fetchH3 failed:", url, e);
    return [];
  }
}
