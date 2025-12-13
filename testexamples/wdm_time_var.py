# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

# 温暗物质温度比列表
T_list = [0.1, 0.4, 0.7, 1.0]
omega_ncdm = 0.1201075
deg_ncdm = 1
colors = ['red', 'orange', 'green', 'blue']

# 创建 output 文件夹
if not os.path.exists("output"):
    os.makedirs("output")

# === 图 1: Lensing φφ ===
plt.figure(figsize=(9, 6))
plt.title("Lensing Potential Spectrum")

for i, Tval in enumerate(T_list):
    tag = "T" + str(Tval).replace('.', '')
    ini_name = "auto_wdm_" + tag + ".ini"
    root_name = "auto_" + tag + "_"

    ini_content = "\n".join([
        "H0 = 67.32117",
        "omega_b = 0.02238280",
        "omega_cdm = 0",
        "omega_ncdm = %.8f" % omega_ncdm,
        "N_ncdm = 1",
        "deg_ncdm = %d" % deg_ncdm,
        "T_ncdm = %.3f" % Tval,
        "YHe = 0.2454006",
        "tau_reio = 0.05430842",
        "n_s = 0.9660499",
        "A_s = 2.100549e-09",
        "lensing = yes",
        "output = tCl,pCl,lCl",
        "write_background = yes",
        "root = output/" + root_name,
        "write parameters = yes",
        "write warnings = yes"
    ])

    with open(ini_name, "w") as f:
        f.write(ini_content)

    print(">>> 正在运行 CLASS for T_ncdm = %.1f" % Tval)
    os.system("./class " + ini_name)

    cl_path = "output/" + root_name + "00_cl_lensed.dat"

    if os.path.exists(cl_path):
        data = np.loadtxt(cl_path)
        ell = data[:, 0]
        Cl_phi_phi = data[:, 5]
        Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
        label = "T/T_nu = %.1f" % Tval
        plt.plot(ell, Dl, label=label, color=colors[i])
    else:
        print("⚠ Output file missing: " + cl_path)

# 添加 CDM-only φφ
cdm_ini = "cdm_reference.ini"
cdm_ini_content = "\n".join([
    "H0 = 67.32117",
    "omega_b = 0.02238280",
    "omega_cdm = 0.1201075",
    "omega_ncdm = 0",
    "YHe = 0.2454006",
    "tau_reio = 0.05430842",
    "n_s = 0.9660499",
    "A_s = 2.100549e-09",
    "lensing = yes",
    "output = tCl,pCl,lCl",
    "root = output/cdm_reference_",
    "write parameters = yes",
    "write warnings = yes"
])
with open(cdm_ini, "w") as f:
    f.write(cdm_ini_content)

print(">>> 正在运行 CLASS for CDM-only")
os.system("./class " + cdm_ini)

cdm_cl_path = "output/cdm_reference_00_cl_lensed.dat"
if os.path.exists(cdm_cl_path):
    data = np.loadtxt(cdm_cl_path)
    ell = data[:, 0]
    Cl_phi_phi = data[:, 5]
    Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
    plt.plot(ell, Dl, label="CDM-only", color='black', linestyle="--")

# 图像设置
plt.xlabel(u"Multipole l")
plt.ylabel(u"l^2 C_l^{phiphi}")
plt.xscale("log")
plt.yscale("log")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("lensing_phi_phi_WDM_by_T.pdf")
plt.show()

# === 图 2: w(z) ===
plt.figure(figsize=(9, 6))
plt.title("Evolution of w_ncdm(z)")

for i, Tval in enumerate(T_list):
    tag = "T" + str(Tval).replace('.', '')
    root_name = "auto_" + tag + "_"
    bkg_path = "output/" + root_name + "00_background.dat"

    if os.path.exists(bkg_path):
        bkg = np.loadtxt(bkg_path)
        z_vals = bkg[:, 0]
        rho_vals = bkg[:, 11]
        p_vals = bkg[:, 12]
        w_vals = p_vals / rho_vals
        label = "T/T_nu = %.1f" % Tval
        plt.plot(z_vals, w_vals, label=label, color=colors[i])
    else:
        print("⚠ Background file missing: " + bkg_path)

plt.xlabel("Redshift z")
plt.ylabel("w_ncdm(z)")
plt.xscale("log")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("w_ncdm_evolution_vs_z.pdf")
plt.show()
