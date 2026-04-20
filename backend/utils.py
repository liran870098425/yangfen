# -*- coding: utf-8 -*-
"""
author:码同学 极光
date:2025/6/27
desc: 
sample: 
"""
import os


def get_project_path():
    """得到项目路径"""
    return os.path.dirname(__file__)

def get_yaml_file_path(file_name):
    """得到files配置路径"""
    return os.path.join(get_project_path(), 'media','yaml',file_name)

def get_yaml_file_folder():
    """得到files配置路径"""
    return os.path.join(get_project_path(), 'media', 'yaml')


#读取路径文件内容
def get_report_content(file_name):
    path= os.path.join(get_yaml_file_folder(), file_name)
    return open(path, 'r', encoding='utf-8').read()

def write_file(path, content):
    # 写入文件
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)