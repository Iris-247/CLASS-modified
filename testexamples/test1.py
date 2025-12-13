# -*- coding: utf-8 -*-
from classy import Class
import numpy as np
import matplotlib.pyplot as plt

# 设置参数
params = {
    'H0': 67.32117,
    'omega_b': 0.02238280,
    'omega_cdm': 0.1201075,
    'N_ur': 2.046,
    'N_ncdm': 1,
    'm_ncdm': 0.06,
    'T_ncdm': 0.7137658555036082,
    'YHe': 0.2454006,
    'tau_reio': 0.05430842,
    'n_s': 0.9660499,
    'A_s': 2.100549e-09,
    'non linear': 'halofit',
    'output': 'tCl,pCl,lCl',
    'lensing': 'yes',
}

# 创建并运行 CLASS
cosmo = Class()
cosmo.set(params)
cosmo.compute()

# 获取 CMB Cl 数据
cls = cosmo.lensed_cl(2500)  # 获取从 l=2 到 l=2500 的谱

# 提取需要的数据
ell = cls['ell'][2:]  # 从 l=2 开始
cl_tt = cls['tt'][2:] * ell * (ell + 1) / (2.0 * np.pi) * 1e12  # 单位: μK^2
cl_ee = cls['ee'][2:] * ell * (ell + 1) / (2.0 * np.pi) * 1e12
cl_te = cls['te'][2:] * ell * (ell + 1) / (2.0 * np.pi) * 1e12

# 开始画图
plt.figure(figsize=(10, 6))
plt.plot(ell, cl_tt, label=r'$C_\ell^{TT}$', color='red')
plt.plot(ell, cl_ee, label=r'$C_\ell^{EE}$', color='blue')
plt.plot(ell, cl_te, label=r'$C_\ell^{TE}$', color='green')
plt.xlabel(r'Multipole $\ell$')
plt.ylabel(r'$\ell(\ell+1)C_\ell/2\pi\ [\mu K^2]$')
plt.title('Lensed CMB Angular Power Spectra')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("cmb_power_spectra.png")
plt.show()

# 清理
cosmo.struct_cleanup()
cosmo.empty()
