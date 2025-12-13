# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os

# 参数设置
T_ncdm = 0.4  # 温暗物质的温度比
density_ratios = [0.1, 1.0, 10.0]
omega_dm_total = 0.1201075
colors = ['red', 'orange', 'green']

# 创建 output 文件夹
if not os.path.exists("output"):
    os.makedirs("output")

# --- 图 1: φφ ---
plt.figure(figsize=(9, 6))
plt.title(u"Lensing Potential Spectrum")

for i, ratio in enumerate(density_ratios):
    omega_cdm = omega_dm_total * ratio / (1.0 + ratio)
    omega_ncdm = omega_dm_total - omega_cdm

    tag = "M%.1f" % ratio
    tag = tag.replace('.', '')
    ini_name = "auto_wdm_" + tag + ".ini"
    root_name = "auto_" + tag + "_"

    ini_content = "\n".join([
        "H0 = 67.32117",
        "omega_b = 0.02238280",
        "omega_cdm = %.8f" % omega_cdm,
        "N_ncdm = 1",
        "omega_ncdm = %.8f" % omega_ncdm,
        "deg_ncdm = 1",
        "T_ncdm = %.3f" % T_ncdm,
        "YHe = 0.2454006",
        "tau_reio = 0.05430842",
        "n_s = 0.9660499",
        "A_s = 2.100549e-09",
        "lensing = yes",
        "output = tCl,pCl,lCl,mPk",
        "P_k_max_h/Mpc = 10",
        "z_pk = 0",
        "root = output/" + root_name,
        "write parameters = yes",
        "write warnings = yes",
        "write background = yes"
    ])

    with open(ini_name, "w") as f:
        f.write(ini_content)

    print(">>> 正在运行 CLASS for rho_cdm/rho_wdm = %.1f" % ratio)
    os.system("./class " + ini_name)

    cl_path = "output/" + root_name + "00_cl_lensed.dat"
    pk_path = "output/" + root_name + "00_pk.dat"

    # --- φφ 图 ---
    if os.path.exists(cl_path):
        data_cl = np.loadtxt(cl_path)
        ell = data_cl[:, 0]
        Cl_phi_phi = data_cl[:, 5]
        Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
        label = u"rho_cdm/rho_wdm = %.1f" % ratio
        plt.plot(ell, Dl, label=label, color=colors[i])
    else:
        print("⚠️ CL 文件缺失：" + cl_path)

# --- 添加 CDM-only ---
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
    "output = tCl,pCl,lCl,mPk",
    "P_k_max_h/Mpc = 10",
    "z_pk = 0",
    "root = output/cdm_reference_",
    "write parameters = yes",
    "write warnings = yes"
])
with open(cdm_ini, "w") as f:
    f.write(cdm_ini_content)
print(">>> 正在运行 CLASS for CDM-only")
os.system("./class " + cdm_ini)

# --- CDM φφ ---
cdm_cl = "output/cdm_reference_00_cl_lensed.dat"
if os.path.exists(cdm_cl):
    data = np.loadtxt(cdm_cl)
    ell = data[:, 0]
    Cl_phi_phi = data[:, 5]
    Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
    plt.plot(ell, Dl, label="CDM-only", color='black', linestyle="--")
else:
    print("⚠️ CDM-only φφ 文件缺失")

# --- 图像配置 φφ ---
plt.xlabel("Multipole l")
plt.ylabel("l^2 C_l^{phiphi}")
plt.xscale("log")
plt.yscale("log")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("lensing_phi_phi_mixed_WDM_CDM_fixed.pdf")

# === 图 2: P(k) ===
plt.figure(figsize=(9, 6))
plt.title(u"Matter Power Spectrum P(k) at z = 0")

for i, ratio in enumerate(density_ratios):
    tag = "M%.1f" % ratio
    tag = tag.replace('.', '')
    root_name = "auto_" + tag + "_"
    pk_path = "output/" + root_name + "00_pk.dat"

    if os.path.exists(pk_path):
        pk_data = np.loadtxt(pk_path)
        k = pk_data[:, 0]
        Pk = pk_data[:, 1]
        label = u"rho_cdm/rho_wdm = %.1f" % ratio
        plt.plot(k, Pk, label=label, color=colors[i])
    else:
        print("⚠️ P(k) 文件缺失：" + pk_path)

# CDM-only P(k)
cdm_pk = "output/cdm_reference_00_pk.dat"
if os.path.exists(cdm_pk):
    pk_data = np.loadtxt(cdm_pk)
    k = pk_data[:, 0]
    Pk = pk_data[:, 1]
    plt.plot(k, Pk, label="CDM-only", color='black', linestyle="--")
else:
    print("⚠️ CDM-only P(k) 文件缺失")

# 图像设置
plt.xlabel("k [h/Mpc]")
plt.ylabel("P(k) [Mpc^3/h^3]")
plt.xscale("log")
plt.yscale("log")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("matter_power_spectrum_mixed_WDM_CDM.pdf")
plt.show()

for i, ratio in enumerate(density_ratios):
    tag = "M%.1f" % ratio
    tag = tag.replace('.', '')
    root_name = "auto_" + tag + "_"
    pk_path = "output/" + root_name + "00_pk.dat"
    bkg_path = os.path.join("output", root_name + "00_background.dat")

    if os.path.exists(bkg_path):
        data = np.loadtxt(bkg_path)
        z = data[:, 0]
        rho = data[:, 11]
        p = data[:, 12]
        w = p / rho

        plt.figure(figsize=(8, 6))
        plt.plot(z, w, label="w(z)", color=colors[i])
        plt.xlabel("Redshift z")
        plt.ylabel("w(z)")
        plt.xscale("log")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.title("w_ncdm(z) for rho_cdm/rho_wdm = %.1f" % ratio)
        plt.legend()
        plt.tight_layout()
        plt.savefig("w_ncdm_mixed_ratio_%s.pdf" % tag)
        plt.close()
    else:
        print("⚠️ 文件不存在，跳过绘制 w(z)：", bkg_path)
