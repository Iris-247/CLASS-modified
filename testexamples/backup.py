# -*- coding: utf-8 -*-
import os
import shutil

# CLASS 根目录
class_dir = "./"  # 请根据你当前路径修改为 CLASS 根目录路径

# 要备份的源代码文件列表（相对路径）
file_list = [
    "source/perturbations.c",
    "include/perturbations.h",
    "source/background.c",
    "include/background.h",
    "source/input.c",
    "include/input.h"
]

# 目标备份文件夹
backup_dir = "backup_ncdm_patch"

# 创建备份目录
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

# 拷贝文件
for rel_path in file_list:
    src = os.path.join(class_dir, rel_path)
    dst = os.path.join(backup_dir, os.path.basename(rel_path))
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print("已备份: %s -> %s" % (src, dst))
    else:
        print("⚠ 未找到: %s" % src)
