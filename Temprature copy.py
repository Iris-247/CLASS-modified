# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import os
import numpy as np
import matplotlib.pyplot as plt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# === 参数设置 ===
f_wdm_list = [0.0, 0.999]
linestyles = ['--', '-.', ':']
gauge_mode = 'new'
model = "ncdmfa_mb"
home = os.path.expanduser("~")
class_dir = os.path.join(home, "class_first_order")
base_output = os.path.join(class_dir, "output")
w_folder_tags = ["1e-6", "1e-5", "1e-4"]

tt_dict = {}

# === 原始谱图 ===
plt.figure(figsize=(9, 6))
plt.title("Temperature Power Spectrum - entropy perturbation")

for w_idx, w_tag in enumerate(w_folder_tags):
    base_dir = os.path.join(base_output, "output_%s_%s_%s" % (model, gauge_mode, w_tag))

    for i, f_wdm in enumerate(f_wdm_list):
        if f_wdm == 0.0:
            tag = "cdm_only_%s" % gauge_mode
        else:
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)

        run_root_abs = os.path.join(base_dir, "%s_%s_" % (model, tag))
        cl_file = run_root_abs + "00_cl.dat"
        if not os.path.exists(cl_file):
            print("⚠️ 未找到文件: %s" % cl_file)
            continue

        data = np.loadtxt(cl_file)
        ell = data[:, 0]
        Cl_tt = data[:, 1]
        Dl_tt = ell * (ell + 1) * Cl_tt / (2 * np.pi)
        key = (w_tag, f_wdm)
        tt_dict[key] = (ell, Dl_tt)

        if abs(f_wdm - 0.999) < 1e-3:
            label = u"$w = 10^{-%s}$" % w_tag.split("e-")[1]
        else:
            label = None

        linestyle = '-' if f_wdm == 0.0 else linestyles[w_idx % len(linestyles)]
        plt.plot(ell, Dl_tt, label=label, color='black', linestyle=linestyle)

plt.xlabel("Multipole $\ell$")
plt.ylabel(u"$\ell(\ell+1)C_\ell^{TT}/(2\pi)\;[\mu K^2]$")
plt.xscale("log")
plt.yscale("log")
plt.tick_params(axis='both', which='both', labelsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()

output_pdf = os.path.join(class_dir, "output", "temperature_tt_%s_%s.pdf" % (model, gauge_mode))
output_png = output_pdf.replace(".pdf", ".png")
plt.savefig(output_pdf)
plt.savefig(output_png, dpi=300)
plt.close()

# === 比值图 ===
plt.figure(figsize=(9, 6))
plt.title("TT Spectrum Ratio to CDM-only")

for w_idx, w_tag in enumerate(w_folder_tags):
    ref_key = (w_tag, 0.0)
    if ref_key not in tt_dict:
        print("⚠️ 缺少 CDM-only 数据: w=%s" % w_tag)
        continue

    ell_ref, Dl_ref = tt_dict[ref_key]

    for i, f_wdm in enumerate(f_wdm_list):
        if f_wdm == 0.0:
            continue
        key = (w_tag, f_wdm)
        if key not in tt_dict:
            continue

        ell, Dl_tt = tt_dict[key]
        ratio = Dl_tt / Dl_ref

        if abs(f_wdm - 0.999) < 1e-3:
            label = u"$w = 10^{-%s}$" % w_tag.split("e-")[1]
        else:
            label = None

        linestyle = linestyles[w_idx % len(linestyles)]
        plt.plot(ell, ratio, label=label, color='black', linestyle=linestyle)

plt.xlabel("Multipole $\ell$")
plt.ylabel(u"$C_\ell^{TT}(\mathrm{WDM}) / C_\ell^{TT}(\mathrm{CDM})$")
plt.xscale("log")
plt.tick_params(axis='both', which='both', labelsize=12)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=12)
plt.tight_layout()

output_pdf_ratio = os.path.join(class_dir, "output", "temperature_tt_ratio_%s_%s.pdf" % (model, gauge_mode))
output_png_ratio = output_pdf_ratio.replace(".pdf", ".png")
plt.savefig(output_pdf_ratio)
plt.savefig(output_png_ratio, dpi=300)
plt.close()
