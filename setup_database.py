import pymysql
import json
import os
from datetime import datetime

# 添加项目路径到sys.path以便能导入env.py
project_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_dir, 'backend')
import sys
sys.path.insert(0, backend_dir)

# 从项目配置文件中读取数据库配置
try:
    from conf.env import (
        DATABASE_HOST,
        DATABASE_PORT,
        DATABASE_USER,
        DATABASE_PASSWORD,
        DATABASE_NAME
    )
    
    DB_CONFIG = {
        'host': DATABASE_HOST,
        'port': DATABASE_PORT,
        'user': DATABASE_USER,
        'password': DATABASE_PASSWORD,
        'database': DATABASE_NAME
    }
except ImportError as e:
    print(f"无法导入数据库配置: {e}")
    exit(1)

def create_database_if_not_exists():
    """创建数据库如果不存在"""
    try:
        # 先连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 `{DB_CONFIG['database']}` 已创建或已存在")
        
        connection.close()
        return True
    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False

def import_json_backup(connection, backup_dir):
    """从JSON文件导入数据"""
    try:
        # 获取所有JSON备份文件
        json_files = [f for f in os.listdir(backup_dir) if f.endswith('.json') and f != 'django_migrations.json']
        
        # 首先处理django_content_type.json，因为它可能被其他表引用
        if 'django_content_type.json' in json_files:
            json_files.remove('django_content_type.json')
            json_files.insert(0, 'django_content_type.json')
        
        for json_file in json_files:
            table_name = json_file.replace('.json', '')
            file_path = os.path.join(backup_dir, json_file)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            data = backup_data.get('data', [])
            if not data:
                print(f"表 {table_name} 没有数据需要导入")
                continue
            
            # 清空表数据
            with connection.cursor() as cursor:
                cursor.execute(f"TRUNCATE TABLE `{table_name}`")
            
            # 构造INSERT语句
            if data:
                columns = list(data[0].keys())
                placeholders = ', '.join(['%s'] * len(columns))
                columns_str = ', '.join([f'`{col}`' for col in columns])
                sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
                
                # 批量插入数据
                with connection.cursor() as cursor:
                    values_list = []
                    for row in data:
                        values = [row[col] for col in columns]
                        values_list.append(values)
                    
                    cursor.executemany(sql, values_list)
                    print(f"表 {table_name} 成功导入 {len(values_list)} 条记录")
            
            connection.commit()
        
        return True
    except Exception as e:
        print(f"导入JSON备份失败: {e}")
        connection.rollback()
        return False

def import_sql_backup(connection, sql_file_path):
    """从SQL文件导入数据"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 分割SQL语句
        sql_statements = sql_content.split(';')
        
        with connection.cursor() as cursor:
            for statement in sql_statements:
                statement = statement.strip()
                if statement and not statement.startswith('--') and not statement.startswith('/*'):
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        # 忽略某些特定错误，比如表已存在的错误
                        if "already exists" not in str(e):
                            print(f"执行SQL语句时出错: {e}")
                            print(f"SQL语句: {statement[:100]}...")
        
        connection.commit()
        print("SQL备份导入完成")
        return True
    except Exception as e:
        print(f"导入SQL备份失败: {e}")
        connection.rollback()
        return False

def main():
    print("开始设置数据库...")
    
    # 1. 创建数据库
    if not create_database_if_not_exists():
        print("无法创建数据库")
        return
    
    # 2. 连接到目标数据库
    try:
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print(f"无法连接到数据库: {e}")
        return
    
    # 3. 导入备份数据
    try:
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups', 'backup_20251115_131332')
        sql_file_path = os.path.join(backup_dir, f"{DB_CONFIG['database']}_backup_20251115_131332.sql")
        
        print("正在导入JSON备份...")
        if import_json_backup(connection, backup_dir):
            print("JSON备份导入成功")
        else:
            print("JSON备份导入失败")
        
        # 如果有SQL文件也尝试导入
        if os.path.exists(sql_file_path):
            print("正在导入SQL备份...")
            if import_sql_backup(connection, sql_file_path):
                print("SQL备份导入成功")
            else:
                print("SQL备份导入失败")
        
        print("数据库设置完成!")
        
    except Exception as e:
        print(f"导入备份过程中出现错误: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()