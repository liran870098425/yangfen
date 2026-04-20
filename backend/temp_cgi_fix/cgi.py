"""
Python 3.13+ 兼容性cgi模块
为解决Django 3.2在Python 3.13+环境下缺少cgi.valid_boundary等问题
"""

import re
from urllib.parse import parse_qs, unquote_plus


def valid_boundary(boundary):
    """验证multipart边界字符串是否有效"""
    if not isinstance(boundary, bytes):
        return False
    if len(boundary) > 70:
        return False
    # 检查边界字符是否合法
    valid_chars = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\'()+_,-./:=?'
    return all(c in valid_chars for c in boundary)


def parse_header(line):
    """解析HTTP头部行"""
    # 简化实现，满足基本需求
    parts = re.split(r';\s*', line.strip())
    if not parts:
        return '', {}
    
    main_value = parts[0]
    params = {}
    
    for part in parts[1:]:
        if '=' in part:
            key, value = part.split('=', 1)
            # 处理引号包裹的值
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            params[key.lower()] = value
    
    return main_value, params


def parse_multipart(fp, boundary, environ):
    """解析multipart数据 - 简化版本"""
    # 这是一个最小实现，实际使用中Django会使用自己的解析器
    # 这里只是为了让cgi模块的基本功能可用
    pass


# 导出必要的函数和类
__all__ = ['valid_boundary', 'parse_header', 'parse_multipart']