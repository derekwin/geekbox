from django.db import models
# from django.contrib.auth import get_user_model
# User=get_user_model()
'''
脱离自带后台，不采用下面方法
Django 为什么在模型中要使用settings.AUTH_USER_MODEL
因为如果A使用from django.contrib.auth import get_user_model
创建外键、一对一、多对多模型，在User的model引用A时就会出现循环引用。
所以错误的方法
from django.contrib.auth import get_user_model
User=get_user_model()
正确姿势
'''
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField


class StikerUser(User):
    created_time=models.DateTimeField(auto_now_add=True)
    InvitedCode=models.CharField(max_length=100, blank=True, null=True)
    GenderChoise=(
        ('None','保密'),
        ('Male','男'),
        ('Female','女')
    )
    Gender = models.CharField(max_length=7,choices=GenderChoise,blank=True, null=True)
    IconChoise=(
        ('1','獾'),
        ('2','熊'),
        ('3','小鸟'),
        ('4','小猫'),
        ('5','毛毛虫'),
        ('6','小狗'),
        ('7','麋鹿'),
        ('8','牛'),
        ('9','大象'),
        ('10','梅花鹿'),
        ('11','大猩猩'),
        ('12','熊猫'),
        ('13','兔子'),
        ('14','鲨鱼'),
        ('15','蜗牛'),
        ('16','独角兽'),
        ('17','鲸鱼'),
        ('16','狼')
    )
    Icon=models.CharField(max_length=7,choices=IconChoise,blank=True, null=True,default=1)
    Introduce_short=models.CharField(max_length=200, blank=True, null=True,verbose_name="个人简介(200字)")
    Introduce=RichTextField(null=True,blank=True,verbose_name="个人说明，更加个性化的个人介绍页面")
    
    
