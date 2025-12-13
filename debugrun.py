# -*- coding: utf-8 -*-
import numpy as np
import os
import shutil
import subprocess

T_ncdm = 0.4
f_wdm_list  = [0.1]
omega_dm_total = 0.1201075
gauge_list = ['synchronous']

def generate_ini_file(f_wdm, ini_path, run_root, gauge):
    omega_ncdm = omega_dm_total * f_wdm
    omega_cdm = omega_dm_total - omega_ncdm
    ini_lines = [
        "H0 = 67.32117",
        "omega_b = 0.02238280",
        "omega_cdm = %.8f" % omega_cdm,
        "YHe = 0.2454006",
        "tau_reio = 0.05430842",
        "n_s = 0.9660499",
        "A_s = 2.100549e-09",
        "lensing = yes",
        "output = tCl,pCl,lCl,mPk",
        "P_k_max_h/Mpc = 10",
        "z_pk = 0",
        "root = %s" % run_root,
        "write background = yes",
        "write parameters = yes",
        "write warnings = yes",
        "gauge = %s" % gauge,
        "k_output_values = 0.01, 0.1, 1.0"
    ]
    if omega_ncdm > 0.0:
        ini_lines.insert(3, "N_ncdm = 1")
        ini_lines.insert(4, "omega_ncdm = %.8f" % omega_ncdm)
        ini_lines.insert(5, "deg_ncdm = 1")
        ini_lines.insert(6, "T_ncdm = %.3f" % T_ncdm)
    with open(ini_path, "w") as f:
        f.write("\n".join(ini_lines))

def run_class(class_dir, ini_filename):
    class_exec = os.path.join(class_dir, "class")
    if not os.path.exists(class_exec):
        print("[错误] 找不到 CLASS 可执行程序: %s" % class_exec)
        return
    if not os.access(class_exec, os.X_OK):
        print("[错误] CLASS 文件存在但没有执行权限，请运行：chmod +x %s" % class_exec)
        return
    status = subprocess.call(["./class", ini_filename], cwd=class_dir)
    if status != 0:
        print("[警告] CLASS 运行失败: %s" % ini_filename)

# 模型信息
perturbation_model = "ncdmfa_mb"
class_dir = "/home/eletr/class_first_order"

for gauge_mode in gauge_list:
    output_subdir = os.path.join(class_dir, "output", "output_%s_%s" % (perturbation_model, gauge_mode))
    if os.path.exists(output_subdir):
        shutil.rmtree(output_subdir)
    os.makedirs(output_subdir)

    for f_wdm in f_wdm_list:
        if f_wdm == 0.0:
            tag = "cdm_only_%s" % gauge_mode
        else:
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)

        ini_filename = "auto_%s_%s.ini" % (perturbation_model, tag)
        ini_path = os.path.join(class_dir, ini_filename)
        run_root = os.path.join("output", "output_%s_%s" % (perturbation_model, gauge_mode), "%s_%s_" % (perturbation_model, tag))
        run_root_abs = os.path.join(class_dir, run_root)
        if not os.path.exists(os.path.dirname(run_root_abs)):
            os.makedirs(os.path.dirname(run_root_abs))

        generate_ini_file(f_wdm, ini_path, run_root, gauge_mode)
        print(">>> 运行 CLASS [%s, gauge=%s]: f_WDM = %.1f" % (perturbation_model, gauge_mode, f_wdm))
        run_class(class_dir, ini_filename)

