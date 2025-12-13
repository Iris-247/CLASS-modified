# -*- coding: utf-8 -*- just for test
import matplotlib
matplotlib.use('Agg')  # 使用无图形界面后端，避免 _tkinter 报错
import matplotlib.pyplot as plt
import numpy as np
import os

# === 图像样式设置 ===
plt.rcParams.update({
    "font.size": 14,
    "lines.linewidth": 2,
    "axes.labelsize": 16,
    "axes.titlesize": 18,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12
})

# === 参数设置 ===
class_dir = "/home/eletr/class_first_order_1"
perturbation_model = "ncdmfa_mb"
f_wdm_list = [0.99]
k_list = [0.01, 0.1, 1.0]
colors = ['black']
gauges = ['new', 'synchronous']

for k in k_list:
    plt.figure(figsize=(9, 6))
    plt.title(u"$\delta_{\mathrm{ncdm}}$ vs $\log_{10}(a)$ at $k=%.2f\;\mathrm{Mpc}^{-1}$" % k)

    for i, f_wdm in enumerate(f_wdm_list):
        for gauge in gauges:
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge)
            k_name = str(int(round(np.log10(k) + 2)))  # e.g., k=0.01 → "0"
            filename = "%s_%s_00_perturbations_k%s_s.dat" % (perturbation_model, tag, k_name)
            data_path = os.path.join(
                class_dir,
                "output",
                "output_%s_%s_1e-5" % (perturbation_model, gauge),
                filename
            )

            try:
                if not os.path.exists(data_path):
                    print("未找到文件:", data_path)
                    continue
                data = np.loadtxt(data_path)
                a = data[:, 1]
                if np.any(a <= 0):
                    print("跳过非正 a 值:", data_path)
                    continue
                loga = np.log10(a)
                delta_ncdm0 = np.log10(np.abs(data[:, 17]))
                style = '-' if gauge == 'new' else '--'
                plt.plot(loga, delta_ncdm0, linestyle=style, color=colors[i])
            except Exception as e:
                print("读取失败:", data_path, str(e))

    # 添加图例说明
    for i, f_wdm in enumerate(f_wdm_list):
        plt.plot([], [], color=colors[i])
    plt.plot([], [], color='black', linestyle='-', label="Newtonian gauge")
    plt.plot([], [], color='black', linestyle='--', label="Synchronous gauge")

    plt.xlabel(u"$\log_{10}(a)$")
    plt.ylabel(u"$\log_{10}|\delta|$")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xlim(-6.5, 0)
    plt.ylim(-2, 5)
    plt.legend()
    plt.tight_layout()

    # 保存图像（兼容 Python 2.7）
    save_base = os.path.join(class_dir, "output", "delta_ncdm_vs_tau_k%.2f" % k)
    dir_path = os.path.dirname(save_base)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    plt.savefig(save_base + ".pdf")
    plt.savefig(save_base + ".png", dpi=300)
    plt.close()

print("✅ 所有图像绘制完毕，已保存为 PDF 与 PNG。")
