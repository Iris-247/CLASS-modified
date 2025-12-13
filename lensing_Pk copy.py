# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')  # 非交互式后端，兼容无桌面环境
import os
import numpy as np
import matplotlib.pyplot as plt

# === 参数设置 ===
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  # Python 2.7 中文兼容

home = os.path.expanduser("~")
class_dir = os.path.join(home, "class_first_order")
base_output_path = os.path.join(class_dir, "output")
perturbation_model = "ncdmfa_mb"
gauge_mode = "new"

f_wdm_list = [0.0, 0.999]
w_folder_tags = ["1e-6", "1e-5", "1e-4"]
cdm_linestyle = '-'
linestyles_wdm = ['--', ':', '-.']

# === Matter Power Spectrum ===
plt.figure(figsize=(9, 6))
plt.title(u"Matter Power Spectrum - entropy perturbation")

for w_idx, w_tag in enumerate(w_folder_tags):
    folder = "output_%s_%s_%s" % (perturbation_model, gauge_mode, w_tag)
    for i, f_wdm in enumerate(f_wdm_list):
        if f_wdm == 0.0:
            tag = "cdm_only_%s" % gauge_mode
            linestyle = cdm_linestyle
            label = None
        else:
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)
            linestyle = linestyles_wdm[w_idx % len(linestyles_wdm)]
            exponent = w_tag.split("e-")[1]
            label = "$w = 10^{-%s}$" % exponent if abs(f_wdm - 0.999) < 1e-3 else None

        run_root = os.path.join(base_output_path, folder, "%s_%s_" % (perturbation_model, tag))
        pk_file = run_root + "00_pk.dat"
        if not os.path.exists(pk_file):
            print("⚠️ 未找到文件：%s" % pk_file)
            continue

        data = np.loadtxt(pk_file)
        k = data[:, 0]
        Pk = data[:, 1]

        plt.plot(k, Pk, label=label, color='black', linestyle=linestyle)

plt.xlabel("$k\;[h/\\mathrm{Mpc}]$")
plt.ylabel("$P(k)\;[\\mathrm{Mpc}^3/h^3]$")
plt.xscale("log")
plt.yscale("log")
plt.tick_params(axis='both', which='both', labelsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(base_output_path, "matter_power_spectrum_%s_%s.png" % (perturbation_model, gauge_mode)))
plt.savefig(os.path.join(base_output_path, "matter_power_spectrum_%s_%s.pdf" % (perturbation_model, gauge_mode)))
plt.close()

# === Lensing φφ Spectrum ===
plt.figure(figsize=(9, 6))
plt.title(u"Lensing $\phi\phi$ Spectrum - entropy perturbation")

for w_idx, w_tag in enumerate(w_folder_tags):
    folder = "output_%s_%s_%s" % (perturbation_model, gauge_mode, w_tag)
    for i, f_wdm in enumerate(f_wdm_list):
        if f_wdm == 0.0:
            tag = "cdm_only_%s" % gauge_mode
            linestyle = cdm_linestyle
            label = None
        else:
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)
            linestyle = linestyles_wdm[w_idx % len(linestyles_wdm)]
            exponent = w_tag.split("e-")[1]
            label = "$w = 10^{-%s}$" % exponent if abs(f_wdm - 0.999) < 1e-3 else None

        run_root = os.path.join(base_output_path, folder, "%s_%s_" % (perturbation_model, tag))
        cl_file = run_root + "00_cl_lensed.dat"
        if not os.path.exists(cl_file):
            print("⚠️ 未找到文件：%s" % cl_file)
            continue

        data = np.loadtxt(cl_file)
        ell = data[:, 0]
        Cl_phi_phi = data[:, 5]
        Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)

        plt.plot(ell, Dl, label=label, color='black', linestyle=linestyle)

plt.xlabel("Multipole $\\ell$")
plt.ylabel("$\\ell^2 C_\\ell^{\\phi\\phi}$")
plt.xscale("log")
plt.yscale("log")
plt.tick_params(axis='both', which='both', labelsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(base_output_path, "lensing_phi_phi_%s_%s.png" % (perturbation_model, gauge_mode)))
plt.savefig(os.path.join(base_output_path, "lensing_phi_phi_%s_%s.pdf" % (perturbation_model, gauge_mode)))
plt.close()
