"""
bsplinen_bary2cart.py

Converts barycentric coordinates in n+1 space to cartesian coordinates
in n-space.

Copyright: C.C. de Visser, Delft University of Technology, 2007
email: c.c.devisser@tudelft.nl
"""

import numpy as np


def bsplinen_bary2cart(simplex: np.ndarray, lam: np.ndarray) -> np.ndarray:
    """Convert barycentric coordinates to cartesian coordinates.

    Parameters
    ----------
    simplex : np.ndarray, shape (n+1, n)
        Vertex coordinates of a simplex in n-space.
        Rows are vertices, columns are coordinates.
    lam : np.ndarray, shape (m, n+1)
        Barycentric coordinates with respect to simplex.

    Returns
    -------
    X : np.ndarray, shape (m, n)
        Global cartesian coordinates. Points with all-positive
        barycentric coordinates lie inside the convex hull of simplex.
    """
    v0 = simplex[0, :]
    # Edge vectors from the reference vertex
    edges = simplex[1:, :] - v0  # shape (n, n)

    # X = v0 + sum_i lambda_i * (v_i - v0)  for i = 1..n
    X = lam[:, 1:] @ edges + v0

    return X
