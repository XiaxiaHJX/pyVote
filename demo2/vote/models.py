from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#定义标题
class VoteHeadline(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    def __str__(self):
        return self.title
    class Meta():
        verbose_name='标题'
        verbose_name_plural=verbose_name

#定义选项
class VoteOption_1(models.Model):
    optionname=models.CharField(max_length=50,verbose_name='选项名字')
    num=models.IntegerField(default=0,verbose_name='总数')
    head=models.ForeignKey(VoteHeadline,on_delete=models.CASCADE,verbose_name='标题')
    def __str__(self):
        return self.optionname
    class Meta():
        verbose_name='选项'
        verbose_name_plural=verbose_name

#定义用户表
# class VoteUser(models.Model):
#     name=models.CharField(max_length=30)
#     pwd=models.CharField(max_length=30)
#     def __str__(self):
#         return self.name

class MyUser(User):
    url =models.URLField(blank=True,null=True,default='http://www.baidu.com')
    class Meta():
        verbose_name='用户'
        verbose_name_plural=verbose_name
