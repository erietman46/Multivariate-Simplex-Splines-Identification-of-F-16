"""
F16_IOmapping.py

Description:
    This file shows how to load and plot the IO mapping of the F16
    aerodynamic coefficient C_m.

Construction date:  17-06-2009
Last updated:       16-03-2026

C.C. de Visser
TUDelft, Faculty of Aerospace Engineering, Division of Control &
Simulation
"""

import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.spatial import Delaunay
import os

# ---- Configuration ----
printfigs = True          # True: save figures to disk as PNG
figpath = ""              # set the path where the figures will be saved

# ---- Loading data ----
dataname = "F16traindata_CMabV_2026.mat"
valdataname = "F16validationdata_2026.mat"

# measurement dataset
train_data = sio.loadmat(dataname)
Cm = train_data["Cm"].flatten()
Z_k = train_data["Z_k"]
U_k = train_data["U_k"]

# special validation dataset
val_data = sio.loadmat(valdataname)
Cm_val = val_data.get("Cm_val")
alpha_val = val_data.get("alpha_val")
beta_val = val_data.get("beta_val")

# measurements Z_k = Z(t) + v(t)
alpha_m = Z_k[:, 0]  # measured angle of attack
beta_m = Z_k[:, 1]   # measured angle of sideslip
Vtot = Z_k[:, 2]     # measured velocity

# input to Kalman filter
Au = U_k[:, 0]  # perfect accelerometer du/dt data
Av = U_k[:, 1]  # perfect accelerometer dv/dt data
Aw = U_k[:, 2]  # perfect accelerometer dw/dt data

# ---- Plotting results ----
plt.close("all")

# create triangulation (only used for plotting here)
tri = Delaunay(Z_k[:, [0, 1]])

# viewing angles
az = 140
el = 36

# --- Figure 101: raw measurements top-down view ---
fig = plt.figure(101, figsize=(9, 5))
fig.patch.set_facecolor("white")
ax = fig.add_subplot(111, projection="3d")
ax.scatter(alpha_m, beta_m, Cm, c="k", marker=".", s=1)
ax.view_init(elev=90, azim=0)
ax.set_xlabel(r"$\alpha$ [rad]")
ax.set_ylabel(r"$\beta$ [rad]")
ax.set_zlabel(r"$C_m$ [-]")
ax.set_title(r"F16 $C_m(\alpha_m, \beta_m)$ raw measurements only")
if printfigs:
    fig.savefig(os.path.join(figpath, "fig_F16data3D.png"), dpi=300)

# --- Figure 1001: triangulated surface + data points ---
fig = plt.figure(1001, figsize=(9, 5))
fig.patch.set_facecolor("white")
ax = fig.add_subplot(111, projection="3d")
ax.plot_trisurf(alpha_m, beta_m, Cm, triangles=tri.simplices,
                cmap="viridis", edgecolor="none", alpha=0.8)
ax.scatter(alpha_m, beta_m, Cm, c="k", marker=".", s=1)
ax.view_init(elev=el, azim=az)
ax.set_xlabel(r"$\alpha$ [rad]")
ax.set_ylabel(r"$\beta$ [rad]")
ax.set_zlabel(r"$C_m$ [-]")
ax.set_title(r"F16 $C_m(\alpha_m, \beta_m)$ raw interpolation")
if printfigs:
    fig.savefig(os.path.join(figpath, "fig_F16data3DSurf.png"), dpi=300)

# --- Validation set plots (if available) ---
if Cm_val is not None:
    Cm_val = Cm_val.flatten()
    alpha_val = alpha_val.flatten()
    beta_val = beta_val.flatten()

    # Figure 2001: validation data 3D
    fig = plt.figure(2001, figsize=(5, 5))
    fig.patch.set_facecolor("white")
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(alpha_val, beta_val, Cm_val, "ro")
    ax.view_init(elev=el, azim=az)
    ax.set_xlabel(r"validation $\alpha$ [rad]")
    ax.set_ylabel(r"validation $\beta$ [rad]")
    ax.set_zlabel(r"validation $C_{m,\mathrm{val}}$ [-]")
    ax.set_title(r"F16 $C_m(\alpha_{\mathrm{val}}, \beta_{\mathrm{val}})$ validation set")
    ax.grid(True)
    if printfigs:
        fig.savefig(os.path.join(figpath, "fig_F16valdata3D.png"), dpi=300)

    # Figure 2002: validation data 2D
    fig = plt.figure(2002, figsize=(5, 5))
    fig.patch.set_facecolor("white")
    plt.plot(alpha_val, beta_val, "ro")
    plt.xlabel(r"validation $\alpha$ [rad]")
    plt.ylabel(r"validation $\beta$ [rad]")
    plt.title(r"F16 $(\alpha_{\mathrm{val}}, \beta_{\mathrm{val}})$ special validation set")
    plt.grid(True)
    if printfigs:
        fig.savefig(os.path.join(figpath, "fig_F16valdata.png"), dpi=300)

plt.show()