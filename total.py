# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import subprocess

T_ncdm = 0.4
f_wdm_list = [0.0, 0.1, 0.3, 0.5, 0.7, 1.0]
omega_dm_total = 0.1201075
colors = ['black', 'red', 'orange', 'green', 'blue', 'purple']
gauge_list = ['new', 'synchronous']

class_paths = {
    "ncdmfa_mb": "/home/iris/class_mb",
    "ncdmfa_CLASS_1st": "/home/iris/class_first_order",
    "ncdmfa_CLASS": "/home/iris/class_origin"
}

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
        "gauge = %s" % gauge
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
        print("[警告] 找不到 CLASS 可执行程序: %s" % class_exec)
        return
    status = subprocess.call(["./class", ini_filename], cwd=class_dir)
    if status != 0:
        print("[警告] CLASS运行失败: %s" % ini_filename)

for perturbation_model, class_dir in class_paths.items():
    for gauge_mode in gauge_list:
        output_subdir = os.path.join(class_dir, "output", "output_%s_%s" % (perturbation_model, gauge_mode))
        if os.path.exists(output_subdir):
            shutil.rmtree(output_subdir)
        os.makedirs(output_subdir)
        cl_data_dict = {}
        tt_data_dict = {}
        plt.figure(figsize=(9, 6))
        plt.title("Lensing Potential Spectrum - %s (%s)" % (perturbation_model, gauge_mode))
        for i, f_wdm in enumerate(f_wdm_list):
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
            cl_path = "%s00_cl_lensed.dat" % run_root_abs
            if os.path.exists(cl_path):
                data_cl = np.loadtxt(cl_path)
                ell = data_cl[:, 0]
                Cl_phi_phi = data_cl[:, 5]
                Dl = ell * (ell + 1)**2 * Cl_phi_phi / (2 * np.pi)
                cl_data_dict[f_wdm] = (ell, Dl)
                label = "f_WDM = %.1f" % f_wdm
                plt.plot(ell, Dl, label=label, color=colors[i])
        plt.xlabel("Multipole l")
        plt.ylabel("$l^2 C_l^{\\phi\\phi}$")
        plt.xscale("log")
        plt.yscale("log")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(class_dir, "output", "lensing_phi_phi_%s_%s.pdf" % (perturbation_model, gauge_mode)))
        plt.close()
        if 0.0 in cl_data_dict:
            ell_ref, Dl_ref = cl_data_dict[0.0]
            plt.figure(figsize=(9, 6))
            plt.title("Lensing Potential Ratio to CDM-only - %s (%s)" % (perturbation_model, gauge_mode))
            for i, f_wdm in enumerate(f_wdm_list):
                if f_wdm == 0.0:
                    continue
                ell, Dl = cl_data_dict[f_wdm]
                ratio = Dl / Dl_ref
                label = "f_WDM = %.1f" % f_wdm
                plt.plot(ell, ratio, label=label, color=colors[i])
            plt.xlabel("Multipole l")
            plt.ylabel("$C_l^{\\phi\\phi}$(WDM) / $C_l^{\\phi\\phi}$(CDM)")
            plt.xscale("log")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(class_dir, "output", "lensing_phi_phi_ratio_%s_%s.pdf" % (perturbation_model, gauge_mode)))
            plt.close()
        plt.figure(figsize=(9, 6))
        plt.title("Temperature Power Spectrum - %s (%s)" % (perturbation_model, gauge_mode))
        for i, f_wdm in enumerate(f_wdm_list):
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)
            run_root = os.path.join(class_dir, "output", "output_%s_%s" % (perturbation_model, gauge_mode), "%s_%s_" % (perturbation_model, tag))
            cl_path = "%s00_cl_lensed.dat" % run_root
            if os.path.exists(cl_path):
                data_cl = np.loadtxt(cl_path)
                ell = data_cl[:, 0]
                Cl_tt = data_cl[:, 1]
                Dl_tt = ell * (ell + 1) * Cl_tt / (2 * np.pi)
                tt_data_dict[f_wdm] = (ell, Dl_tt)
                label = "f_WDM = %.1f" % f_wdm
                plt.plot(ell, Dl_tt, label=label, color=colors[i])
        plt.xlabel("Multipole l")
        plt.ylabel("$l(l+1)C_l^{TT}/(2\\pi)$ [$\\mu K^2$]")
        plt.xscale("log")
        plt.yscale("log")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(class_dir, "output", "temperature_tt_%s_%s.pdf" % (perturbation_model, gauge_mode)))
        plt.close()
        if 0.0 in tt_data_dict:
            ell_ref, Dl_tt_ref = tt_data_dict[0.0]
            plt.figure(figsize=(9, 6))
            plt.title("Temperature Spectrum Ratio to CDM-only - %s (%s)" % (perturbation_model, gauge_mode))
            for i, f_wdm in enumerate(f_wdm_list):
                if f_wdm == 0.0:
                    continue
                ell, Dl_tt = tt_data_dict[f_wdm]
                ratio_tt = Dl_tt / Dl_tt_ref
                label = "f_WDM = %.1f" % f_wdm
                plt.plot(ell, ratio_tt, label=label, color=colors[i])
            plt.xlabel("Multipole l")
            plt.ylabel("$C_l^{TT}$(WDM) / $C_l^{TT}$(CDM)")
            plt.xscale("log")
            plt.grid(True, linestyle="--", alpha=0.5)
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(class_dir, "output", "temperature_tt_ratio_%s_%s.pdf" % (perturbation_model, gauge_mode)))
            plt.close()
        plt.figure(figsize=(9, 6))
        plt.title("Matter Power Spectrum - %s (%s)" % (perturbation_model, gauge_mode))
        for i, f_wdm in enumerate(f_wdm_list):
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)
            run_root = os.path.join(class_dir, "output", "output_%s_%s" % (perturbation_model, gauge_mode), "%s_%s_" % (perturbation_model, tag))
            pk_path = "%s00_pk.dat" % run_root
            if os.path.exists(pk_path):
                pk_data = np.loadtxt(pk_path)
                k = pk_data[:, 0]
                Pk = pk_data[:, 1]
                label = "f_WDM = %.1f" % f_wdm
                plt.plot(k, Pk, label=label, color=colors[i])
        plt.xlabel("$k\;[h/\\mathrm{Mpc}]$")
        plt.ylabel("$P(k)\;[\\mathrm{Mpc}^3/h^3]$")
        plt.xscale("log")
        plt.yscale("log")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(class_dir, "output", "matter_power_spectrum_%s_%s.pdf" % (perturbation_model, gauge_mode)))
        plt.close()
        for i, f_wdm in enumerate(f_wdm_list):
            tag = "fw%d_%s" % (int(f_wdm * 100), gauge_mode)
            run_root = os.path.join(class_dir, "output", "output_%s_%s" % (perturbation_model, gauge_mode), "%s_%s_" % (perturbation_model, tag))
            bkg_path = "%s00_background.dat" % run_root
            if os.path.exists(bkg_path):
                data = np.loadtxt(bkg_path)
                z = data[:, 0]
                rho = data[:, 11]
                p = data[:, 12]
                w = p / rho
                plt.figure(figsize=(8, 6))
                plt.plot(z, w, label="f_WDM = %.1f" % f_wdm, color=colors[i])
                plt.xlabel("Redshift z")
                plt.ylabel("$w(z)$")
                plt.xscale("log")
                plt.grid(True, linestyle="--", alpha=0.5)
                plt.title("w_ncdm(z) - %s (%s)" % (perturbation_model, gauge_mode))
                plt.legend()
                plt.tight_layout()
                plt.savefig(os.path.join(class_dir, "output", "w_ncdm_%s_%s.pdf" % (tag, gauge_mode)))
                plt.close()