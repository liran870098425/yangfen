import json

from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.models import ProjectInfo, ModuleInfo
from base.serializers import ProjectInfoSerializer, ModuleInfoSerializer
from dvadmin.utils.RequestUtil import RequestUtil
from dvadmin.utils.json_response import DetailResponse, ErrorResponse, SuccessResponse
from dvadmin.utils.string_util import load_json
from dvadmin.utils.viewset import CustomModelViewSet


class ProjectInfoView(CustomModelViewSet):
    queryset = ProjectInfo.objects.all()
    serializer_class = ProjectInfoSerializer
    
    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def sync_data(self, request):
        """
        Synchronize project and module data
        """
        try:
            # Get data from request
            projects_data = request.data.get('projects', [])
            modules_data = request.data.get('modules', [])
            
            # Sync projects
            project_mapping = {}
            for project_data in projects_data:
                project_id = project_data.get('id')
                project_name = project_data.get('project_name')
                
                if project_id:
                    # Update existing project
                    try:
                        project = ProjectInfo.objects.get(id=project_id)
                        project.project_name = project_name
                        project.publish_app = project_data.get('publish_app', '')
                        project.save()
                    except ProjectInfo.DoesNotExist:
                        # Create new project if not exists
                        project = ProjectInfo.objects.create(
                            id=project_id,
                            project_name=project_name,
                            publish_app=project_data.get('publish_app', '')
                        )
                else:
                    # Create new project
                    project = ProjectInfo.objects.create(
                        project_name=project_name,
                        publish_app=project_data.get('publish_app', '')
                    )
                
                project_mapping[project_data.get('original_id') or project_id] = project.id
            
            # Sync modules
            for module_data in modules_data:
                module_id = module_data.get('id')
                module_name = module_data.get('module_name')
                project_original_id = module_data.get('project_belong')
                
                # Map the project id
                project_id = project_mapping.get(project_original_id, project_original_id)
                
                if module_id:
                    # Update existing module
                    try:
                        module = ModuleInfo.objects.get(id=module_id)
                        module.module_name = module_name
                        if project_id:
                            try:
                                project = ProjectInfo.objects.get(id=project_id)
                                module.project_belong = project
                            except ProjectInfo.DoesNotExist:
                                pass
                        module.save()
                    except ModuleInfo.DoesNotExist:
                        # Create new module if not exists
                        module = ModuleInfo.objects.create(
                            id=module_id,
                            module_name=module_name
                        )
                        if project_id:
                            try:
                                project = ProjectInfo.objects.get(id=project_id)
                                module.project_belong = project
                                module.save()
                            except ProjectInfo.DoesNotExist:
                                pass
                else:
                    # Create new module
                    module = ModuleInfo.objects.create(
                        module_name=module_name
                    )
                    if project_id:
                        try:
                            project = ProjectInfo.objects.get(id=project_id)
                            module.project_belong = project
                            module.save()
                        except ProjectInfo.DoesNotExist:
                            pass
            
            return SuccessResponse(msg="数据同步成功")
        except Exception as e:
            return ErrorResponse(msg=f"数据同步失败: {str(e)}")


class ModuleInfoView(CustomModelViewSet):
    queryset = ModuleInfo.objects.all()
    serializer_class = ModuleInfoSerializer