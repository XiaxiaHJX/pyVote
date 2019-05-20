from django.db import models

# Create your models here.

#定义标题
class VoteHeadline(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    def __str__(self):
        return self.title

#定义选项
class VoteOption_1(models.Model):
    optionname=models.CharField(max_length=50,verbose_name='选项名字')
    num=models.IntegerField(default=0,verbose_name='总数')
    head=models.ForeignKey(VoteHeadline,on_delete=models.CASCADE,verbose_name='标题')
    def __str__(self):
        return self.optionname

#定义用户表
class VoteUser(models.Model):
    name=models.CharField(max_length=30)
    pwd=models.IntegerField()

    def __str__(self):
        return self.name

