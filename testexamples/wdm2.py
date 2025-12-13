# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
T_ncdm = [0.4, 0.7]
density_ratios = [0.1, 1.0, 10.0]
omega_ncdm_total = 0.1201075
deg_ncdm = 1
colors = ['red', 'orange', 'green']

if not os.path.exists("output"):
    os.makedirs("output")

plt_phi = plt.figure(figsize=(9, 6))
plt.title("Lensing Potential Spectrum")

plt_mpk = plt.figure(figsize=(9, 6))
ax_mpk = plt.gca()
plt.title("Matter Power Spectrum at z=0")

for i in range(len(density_ratios)):
    ratio = density_ratios[i]
    omega_ncdm_1 = omega_ncdm_total / (1 + ratio)
    omega_ncdm_2 = omega_ncdm_total - omega_ncdm_1
    omega_list = [omega_ncdm_1, omega_ncdm_2]

    tag = "R%.1f" % ratio
    tag = tag.replace('.', '')
    ini_name = "auto_wdm_" + tag + ".ini"
    root_name = "output/auto_" + tag + "_"

    ini_content = "\n".join([
        "H0 = 67.32117",
        "omega_b = 0.02238280",
        "omega_cdm = 0",
        "N_ncdm = 2",
        "omega_ncdm = %.8f, %.8f" % (omega_list[0], omega_list[1]),
        "deg_ncdm = %d, %d" % (deg_ncdm, deg_ncdm),
        "T_ncdm = %.3f, %.3f" % (T_ncdm[0], T_ncdm[1]),
        "YHe = 0.2454006",
        "tau_reio = 0.05430842",
        "n_s = 0.9660499",
        "A_s = 2.100549e-09",
        "P_k_max_h/Mpc = 10",
        "lensing = yes",
        "output = tCl,pCl,lCl,mPk",
        "z_pk = 0",
        "root = " + root_name,
        "write parameters = yes",
        "write warnings = yes",
        "write_background = yes"
    ])

    with open(ini_name, "w") as f_ini:
        f_ini.write(ini_content)

    print(">>> 正在运行 CLASS for rho_1/rho_2 = %.1f" % ratio)
    os.system("./class " + ini_name)

    cl_path = root_name + "00_cl_lensed.dat"
    if os.path.exists(cl_path):
        data = np.loadtxt(cl_path)
        ell = data[:, 0]
        Cl_phi_phi = data[:, 5]
        Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
        plt.figure(plt_phi.number)
        plt.plot(ell, Dl, label="rho_1/rho_2 = %.1f" % ratio, color=colors[i])
    else:
        print("phi-phi 输出文件缺失：", cl_path)

    pk_path = root_name + "00_pk.dat"
    if os.path.exists(pk_path):
        data = np.loadtxt(pk_path)
        k = data[:, 0]
        Pk = data[:, 1]
        plt.figure(plt_mpk.number)
        ax_mpk.plot(k, Pk, label="rho_1/rho_2 = %.1f" % ratio, color=colors[i])
    else:
        print("P(k) 输出文件缺失：", pk_path)

    bkg_path = root_name + "00_background.dat"
    if os.path.exists(bkg_path):
        data = np.loadtxt(bkg_path)
        z_vals = data[:, 0]
        rho_1 = data[:, 11]
        p_1 = data[:, 12]
        rho_2 = data[:, 13]
        p_2 = data[:, 14]
        w1 = p_1 / rho_1
        w2 = p_2 / rho_2

        plt.figure(figsize=(9, 6))
        plt.plot(z_vals, w1, label="w_ncdm(1)", color=colors[0])
        plt.plot(z_vals, w2, label="w_ncdm(2)", color=colors[1])
        plt.xlabel("Redshift z")
        plt.ylabel("w(z)")
        plt.title("w_ncdm(z) for rho_1/rho_2 = %.1f" % ratio)
        plt.xscale("log")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("w_ncdm_evolution_ratio_%s.pdf" % tag)
        plt.close()

cdm_ini = "cdm_reference.ini"
cdm_root = "output/cdm_reference_"
cdm_ini_content = "\n".join([
    "H0 = 67.32117",
    "omega_b = 0.02238280",
    "omega_cdm = 0.1201075",
    "YHe = 0.2454006",
    "tau_reio = 0.05430842",
    "n_s = 0.9660499",
    "A_s = 2.100549e-09",
    "P_k_max_h/Mpc = 10",
    "lensing = yes",
    "output = tCl,pCl,lCl,mPk",
    "z_pk = 0",
    "root = " + cdm_root,
    "write parameters = yes",
    "write warnings = yes",
    "write_background = yes"
])
with open(cdm_ini, "w") as f:
    f.write(cdm_ini_content)

print(">>> 正在运行 CLASS for CDM-only")
os.system("./class " + cdm_ini)

cdm_cl_path = cdm_root + "00_cl_lensed.dat"
if os.path.exists(cdm_cl_path):
    data = np.loadtxt(cdm_cl_path)
    ell = data[:, 0]
    Cl_phi_phi = data[:, 5]
    Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
    plt.figure(plt_phi.number)
    plt.plot(ell, Dl, label="CDM-only", color='black', linestyle="--")

cdm_pk_path = cdm_root + "00_pk.dat"
if os.path.exists(cdm_pk_path):
    data = np.loadtxt(cdm_pk_path)
    k = data[:, 0]
    Pk = data[:, 1]
    plt.figure(plt_mpk.number)
    ax_mpk.plot(k, Pk, label="CDM-only", color='black', linestyle="--")

plt.figure(plt_phi.number)
plt.xlabel("ell")
plt.ylabel("ell^2 C_ell^{phiphi} [muK^2]")
plt.xscale("log")
plt.yscale("log")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("lensing_phi_phi_mixed_WDM_CDM_ref.pdf")

plt.figure(plt_mpk.number)
ax_mpk.set_xlabel("k [h/Mpc]")
ax_mpk.set_ylabel("P(k) [Mpc^3/h^3]")
ax_mpk.set_xscale("log")
ax_mpk.set_yscale("log")
ax_mpk.grid(True, linestyle="--", alpha=0.5)
ax_mpk.legend()
plt.tight_layout()
plt.savefig("matter_power_spectrum_mixed_WDM_CDM_ref.pdf")
plt.show()
