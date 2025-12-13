from setuptools import setup
from setuptools import Extension
from Cython.Distutils import build_ext

import numpy as nm
import os
import subprocess as sbp
import os.path as osp
import sys

# 获取 gcc 的库路径（无 decode）
GCCPATH_STRING = sbp.check_output(['gcc', '-print-libgcc-file-name'])
GCCPATH = os.path.dirname(GCCPATH_STRING.strip())

# 链接库列表，默认需要 class，如果系统支持 mvec 就加上
liblist = ["class"]
MVEC_STRING = sbp.Popen(['gcc', '-lmvec'], stderr=sbp.PIPE).communicate()[1]
if b"mvec" not in MVEC_STRING:
    liblist += ["mvec", "m"]

# 设置路径
this_dir = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.abspath(os.path.join(this_dir, ".."))
include_folder = os.path.join(root_folder, "include")
classy_folder = os.path.join(root_folder, "python")
heat_folder = os.path.join(root_folder, "external", "heating")
recfast_folder = os.path.join(root_folder, "external", "RecfastCLASS")
hyrec_folder = os.path.join(root_folder, "external", "HyRec2020")
hmcode_folder = os.path.join(root_folder, "external", "HMcode")
halofit_folder = os.path.join(root_folder, "external", "Halofit")

# 检查 libclass.a 是否存在
libclass_path = os.path.join(root_folder, "libclass.a")
if not os.path.exists(libclass_path):
    raise RuntimeError("Missing libclass.a. Please run 'make' in the CLASS root directory first.")

# 提取版本号
with open(os.path.join(include_folder, 'common.h'), 'r') as v_file:
    for line in v_file:
        if '_VERSION_' in line:
            VERSION = line.split()[-1].strip('"v\n')
            break
    else:
        VERSION = "unknown"

# 定义 Cython 扩展
classy_ext = Extension(
    "classy",
    [os.path.join(classy_folder, "classy.pyx")],
    include_dirs=[
        nm.get_include(), include_folder,
        heat_folder, recfast_folder, hyrec_folder,
        hmcode_folder, halofit_folder
    ],
    libraries=liblist,
    library_dirs=[root_folder, GCCPATH],
    language="c++",
    extra_compile_args=["-std=c++11"]
)

# 设置语言级别
classy_ext.cython_directives = {'language_level': "2"}

# 调用 setuptools 安装
setup(
    name='classy',
    version=VERSION,
    description='Python interface to the Cosmological Boltzmann code CLASS',
    url='http://www.class-code.net',
    cmdclass={'build_ext': build_ext},
    ext_modules=[classy_ext],
)
