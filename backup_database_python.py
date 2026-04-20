import pymysql
import json
import os
import sys
from datetime import datetime

# 添加项目路径到sys.path以便能导入env.py
project_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_dir, 'backend')
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
    # 使用默认配置作为后备
    DB_CONFIG = {
        'host': '127.0.0.1',
        'port': 3311,
        'user': 'root',
        'password': '123456',
        'database': 'testplatform'
    }

def connect_database():
    """连接到数据库"""
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
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def get_all_tables(connection):
    """获取所有表名"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            # MySQL的SHOW TABLES结果中的键是"Tables_in_{database_name}"
            table_key = f"Tables_in_{DB_CONFIG['database']}"
            return [table[table_key] for table in tables]
    except Exception as e:
        print(f"获取表列表失败: {e}")
        return []

def backup_table_to_json(connection, table_name, backup_dir):
    """将单个表备份为JSON格式"""
    try:
        with connection.cursor() as cursor:
            # 获取表数据
            cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = cursor.fetchall()
            
            # 获取表结构
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            create_table_sql = cursor.fetchone()
            
            # 创建备份数据结构
            backup_data = {
                'table_name': table_name,
                'create_table_sql': create_table_sql[f'Create Table'],
                'data': rows,
                'backup_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 写入JSON文件
            filename = os.path.join(backup_dir, f"{table_name}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"表 {table_name} 备份完成，共 {len(rows)} 条记录")
            return True
    except Exception as e:
        print(f"备份表 {table_name} 失败: {e}")
        return False

def backup_database_to_sql(connection, backup_dir, filename):
    """将整个数据库备份为SQL格式"""
    try:
        filepath = os.path.join(backup_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"-- Database backup for {DB_CONFIG['database']}\n")
            f.write(f"-- Backup time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            tables = get_all_tables(connection)
            for table_name in tables:
                f.write(f"-- Table structure for table `{table_name}`\n")
                
                # 获取表结构
                with connection.cursor() as cursor:
                    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                    create_table_sql = cursor.fetchone()
                    f.write(f"{create_table_sql[f'Create Table']};\n\n")
                
                # 备份数据
                f.write(f"-- Data for table `{table_name}`\n")
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM `{table_name}`")
                    rows = cursor.fetchall()
                    
                    if rows:
                        # 获取列名
                        columns = list(rows[0].keys())
                        f.write(f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}) VALUES\n")
                        
                        # 写入数据行
                        for i, row in enumerate(rows):
                            values = []
                            for col in columns:
                                if row[col] is None:
                                    values.append('NULL')
                                elif isinstance(row[col], (int, float)):
                                    values.append(str(row[col]))
                                else:
                                    # 转义单引号并包装字符串
                                    escaped_value = str(row[col]).replace("'", "''")
                                    values.append(f"'{escaped_value}'")
                            
                            line_end = ',\n' if i < len(rows) - 1 else ';\n'
                            f.write(f"  ({', '.join(values)}){line_end}")
                    else:
                        f.write(f"-- Table `{table_name}` is empty\n")
                    
                    f.write('\n')
        
        print(f"数据库 SQL 备份完成: {filename}")
        return True
    except Exception as e:
        print(f"数据库 SQL 备份失败: {e}")
        return False

def main():
    print("开始数据库备份...")
    
    # 创建备份目录
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(backup_dir, f"backup_{timestamp}")
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # 连接数据库
    connection = connect_database()
    if not connection:
        print("无法连接到数据库，备份失败")
        return
    
    try:
        print(f"备份文件将保存到: {backup_dir}")
        
        # 方案1: 为每个表创建JSON备份文件
        print("\n开始 JSON 格式备份...")
        tables = get_all_tables(connection)
        json_backup_success = True
        
        for table_name in tables:
            if not backup_table_to_json(connection, table_name, backup_dir):
                json_backup_success = False
        
        if json_backup_success:
            print("JSON 格式备份完成")
        else:
            print("JSON 格式备份过程中出现错误")
        
        # 方案2: 创建完整的SQL备份文件
        print("\n开始 SQL 格式备份...")
        sql_filename = f"{DB_CONFIG['database']}_backup_{timestamp}.sql"
        if backup_database_to_sql(connection, backup_dir, sql_filename):
            print("SQL 格式备份完成")
        else:
            print("SQL 格式备份失败")
        
        print(f"\n备份完成! 文件保存在: {backup_dir}")
        
    except Exception as e:
        print(f"备份过程中出现错误: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()