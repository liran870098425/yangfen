from django.db import models

# Create your models here.
#测试环境维护
from dvadmin.system.models import Users
from dvadmin.utils.models import CoreModel


#测试工程维护
class ProjectInfo(CoreModel):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'base_projectinfo'

    project_name = models.CharField(verbose_name='项目名称', max_length=50, unique=True, null=False)
    responsible_user = models.ManyToManyField(to=Users, related_name='user1',null=True, blank=True, db_constraint=False,
                                    verbose_name="负责人")
    publish_app = models.CharField(verbose_name='发布应用', max_length=100, null=True, blank=True)

#模块
class ModuleInfo(CoreModel):
    class Meta:
        verbose_name = '模块信息'
        db_table = 'base_moduleinfo'

    module_name = models.CharField(verbose_name='模块名称',max_length=50, null=False,unique=True)
    #select 1对多
    project_belong = models.ForeignKey(
        to="ProjectInfo",
        verbose_name="所属项目",
        on_delete=models.CASCADE,
        db_constraint=False
    )
    #table-select 多对多
    test_user = models.ManyToManyField(to=Users, verbose_name='测试人员', related_name='user2', max_length=100, null=True,
                                       blank=True, db_constraint=False)