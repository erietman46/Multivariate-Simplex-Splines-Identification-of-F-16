"""
bsplinen_cart2bary.py

Converts cartesian coordinates in n-space to barycentric coordinates
in n+1 space.

Copyright: C.C. de Visser, Delft University of Technology, 2007
email: c.c.devisser@tudelft.nl
"""

import numpy as np
from numpy.linalg import solve


def bsplinen_cart2bary(simplex: np.ndarray, X: np.ndarray) -> np.ndarray:
    """Convert cartesian coordinates to barycentric coordinates.

    Parameters
    ----------
    simplex : np.ndarray, shape (n+1, n)
        Vertex coordinates of a simplex in n-space.
        Rows are vertices, columns are coordinates.
    X : np.ndarray, shape (m, n)
        Points in n-space in cartesian coordinates.

    Returns
    -------
    Lambda : np.ndarray, shape (m, n+1)
        Barycentric coordinates of X with respect to simplex.
        All-positive rows indicate points inside the convex hull;
        any negative value means the point is outside.
    """
    # Reference vertex is the first simplex vertex
    v0 = simplex[0, :]
    vcount2 = simplex.shape[0] - 1
    Xcount = X.shape[0]
    Lambda = np.zeros((Xcount, vcount2 + 1))

    # Assemble matrix A: columns are edge vectors from v0
    A = (simplex[1:, :] - v0).T  # shape (n, n)

    for i in range(Xcount):
        # Relative coordinates of x
        p = X[i, :] - v0

        # Last n barycentric coordinates
        lambda1 = solve(A, p)

        # First barycentric coordinate
        lambda0 = 1.0 - np.sum(lambda1)

        Lambda[i, 0] = lambda0
        Lambda[i, 1:] = lambda1

    return Lambda