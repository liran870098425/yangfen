import json
import os
import sys
import django

# 添加项目路径到sys.path以便能导入配置
project_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_dir, 'backend')
sys.path.insert(0, backend_dir)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.core import serializers
from django.db import transaction
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

def load_json_data(file_path):
    """Load JSON data from backup file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def import_table_data(model_name, data):
    """Import data for a specific model"""
    try:
        # Get the model class
        app_label, model_label = model_name.split('.')
        model = apps.get_model(app_label, model_label)
        
        # Delete existing data
        model.objects.all().delete()
        
        # Create new objects
        for item in data:
            # Handle special fields
            if 'pk' in item:
                item['id'] = item.pop('pk')
                
            # Handle datetime fields if needed
            model.objects.create(**item)
            
        print(f"Successfully imported {len(data)} records into {model_name}")
        return True
    except Exception as e:
        print(f"Error importing {model_name}: {e}")
        return False

def main():
    print("Starting backup import...")
    
    # Directory with backup files
    backup_dir = os.path.join(project_dir, 'backups', 'backup_20251115_131332')
    
    # List of files to import in order (important for foreign key relationships)
    import_order = [
        'django_content_type.json',
        'auth_permission.json',
        'dvadmin_system_users.json',
        'auth_group.json',
        'dvadmin_system_dept.json',
        'dvadmin_system_role.json',
        'dvadmin_system_menu.json',
        'dvadmin_system_post.json',
        'dvadmin_system_dictionary.json',
        'dvadmin_system_config.json',
        'base_projectinfo.json',
        'base_moduleinfo.json',
        'auth_group_permissions.json',
        'dvadmin_system_users_groups.json',
        'dvadmin_system_users_post.json',
        'dvadmin_system_users_role.json',
        'dvadmin_system_users_user_permissions.json',
        'base_projectinfo_responsible_user.json',
        'base_moduleinfo_test_user.json',
        'dvadmin_system_role_menu.json',
        'dvadmin_system_role_dept.json',
        'dvadmin_system_role_permission.json',
        'dvadmin_system_area.json',
        'dvadmin_system_file_list.json',
        'dvadmin_system_login_log.json',
        'dvadmin_system_operation_log.json',
        'dvadmin_system_menu_button.json',
        'dvadmin_message_center.json',
        'dvadmin_message_center_target_user.json',
        'dvadmin_message_center_target_role.json',
        'dvadmin_message_center_target_dept.json',
        'dvadmin_api_white_list.json',
        'captcha_captchastore.json',
        'django_session.json',
        'token_blacklist_outstandingtoken.json',
        'token_blacklist_blacklistedtoken.json'
    ]
    
    # Import data
    with transaction.atomic():
        for filename in import_order:
            file_path = os.path.join(backup_dir, filename)
            if os.path.exists(file_path):
                print(f"Importing {filename}...")
                try:
                    backup_data = load_json_data(file_path)
                    data = backup_data.get('data', [])
                    table_name = filename.replace('.json', '')
                    
                    # Map table names to Django models
                    model_mapping = {
                        'auth_group': 'auth.Group',
                        'auth_permission': 'auth.Permission',
                        'django_content_type': 'contenttypes.ContentType',
                        'django_session': 'sessions.Session',
                        'base_moduleinfo': 'base.ModuleInfo',
                        'base_projectinfo': 'base.ProjectInfo',
                        'dvadmin_system_users': 'system.Users',
                        'dvadmin_system_dept': 'system.Dept',
                        'dvadmin_system_role': 'system.Role',
                        'dvadmin_system_menu': 'system.Menu',
                        'dvadmin_system_post': 'system.Post',
                        'dvadmin_system_dictionary': 'system.Dictionary',
                        'dvadmin_system_config': 'system.SystemConfig',
                        'dvadmin_system_area': 'system.Area',
                        'dvadmin_system_file_list': 'system.FileList',
                        'dvadmin_system_login_log': 'system.LoginLog',
                        'dvadmin_system_operation_log': 'system.OperationLog',
                        'dvadmin_system_menu_button': 'system.MenuButton',
                        'dvadmin_message_center': 'system.MessageCenter',
                        'dvadmin_api_white_list': 'system.ApiWhiteList',
                        'captcha_captchastore': 'captcha.CaptchaStore',
                        'token_blacklist_outstandingtoken': 'token_blacklist.OutstandingToken',
                        'token_blacklist_blacklistedtoken': 'token_blacklist.BlacklistedToken',
                        # Many-to-many relationship tables
                        'auth_group_permissions': None,
                        'base_moduleinfo_test_user': None,
                        'base_projectinfo_responsible_user': None,
                        'dvadmin_system_users_groups': None,
                        'dvadmin_system_users_post': None,
                        'dvadmin_system_users_role': None,
                        'dvadmin_system_users_user_permissions': None,
                        'dvadmin_system_role_menu': None,
                        'dvadmin_system_role_dept': None,
                        'dvadmin_system_role_permission': None,
                        'dvadmin_message_center_target_user': None,
                        'dvadmin_message_center_target_role': None,
                        'dvadmin_message_center_target_dept': None,
                        'django_migrations': None,  # Skip migrations
                    }
                    
                    model_name = model_mapping.get(table_name)
                    if model_name and data:
                        # For tables with actual models
                        for item in data:
                            try:
                                # Handle special fields
                                if 'pk' in item:
                                    item['id'] = item.pop('pk')
                                    
                                # Get the model class
                                app_label, model_label = model_name.split('.')
                                model = apps.get_model(app_label, model_label)
                                
                                # Create or update the object
                                obj, created = model.objects.update_or_create(
                                    id=item['id'],
                                    defaults=item
                                )
                            except Exception as e:
                                print(f"Error importing item in {table_name}: {e}")
                                continue
                                
                        print(f"Successfully imported {len(data)} records into {table_name}")
                    else:
                        # Handle many-to-many relationship tables or skipped tables
                        print(f"Skipped {filename} (relationship table or skipped)")
                        
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    continue
            else:
                print(f"File not found: {filename}")
    
    print("Backup import completed!")

if __name__ == "__main__":
    main()