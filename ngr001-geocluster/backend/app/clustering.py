"""
Clustering Algorithms Module

This module implements spatial clustering algorithms for the NGR001 Geospatial
Event Clustering System. It provides two clustering approaches:
    - H3 hexagonal binning for hierarchical spatial aggregation
    - DBSCAN density-based clustering with Haversine distance

Functions:
    h3_bin: Aggregate points into H3 hexagonal bins
    dbscan_haversine: Cluster points using DBSCAN with geographic distance
"""

import numpy as np
from sklearn.cluster import DBSCAN
import h3

EARTH_M = 6371000.0
"""Earth's radius in meters, used for Haversine distance calculations."""


def _to_radians(points):
    """
    Convert latitude/longitude points to radians for Haversine calculations.
    
    Args:
        points: List of (lat, lon) tuples in degrees
    
    Returns:
        NumPy array of points in radians
    """
    arr = np.radians(np.array([[p[0], p[1]] for p in points]))
    return arr


def dbscan_haversine(points, eps_m=500, min_samples=5):
    """
    Perform DBSCAN clustering using Haversine (great-circle) distance.
    
    This function clusters geographic points based on their actual distance
    on Earth's surface, accounting for the spherical geometry.
    
    Args:
        points: List of (lat, lon) tuples
        eps_m: Maximum distance (in meters) between points in a cluster
        min_samples: Minimum points required to form a cluster
    
    Returns:
        NumPy array of cluster labels (-1 indicates noise/outlier)
    """
    X = _to_radians(points)
    eps = eps_m / EARTH_M
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine')
    labels = db.fit_predict(X)
    return labels


def h3_bin(points, res=7):
    """
    Aggregate geographic points into H3 hexagonal bins.
    
    H3 is Uber's hierarchical hexagonal spatial indexing system. This function
    assigns each point to an H3 cell and counts the number of points per cell.
    
    Args:
        points: List of (lat, lon) tuples
        res: H3 resolution level (0-15, higher = smaller hexagons)
             Resolution 7 produces hexagons ~5km across
    
    Returns:
        Dictionary mapping H3 cell indices to point counts
    """
    bins = {}
    for lat, lon in points:
        idx = h3.geo_to_h3(lat, lon, res)
        bins[idx] = bins.get(idx, 0) + 1
    return bins
