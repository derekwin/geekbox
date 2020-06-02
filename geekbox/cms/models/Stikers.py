from django.db import models 
from .Users import StikerUser

from ckeditor.fields import RichTextField


class Topic(models.Model):
    '''
    话题
    '''
    name = models.CharField(max_length=100, blank=True, null=True,verbose_name='话题')
    help_text=RichTextField(null=True,blank=True)
    class Meta:
        verbose_name='话题'
        verbose_name_plural="话题"


    def __str__(self):
        return str(self.name)

    


class Stiker(models.Model):
    '''
    贴
    '''
    title = models.CharField(max_length=200, blank=True, null=True,verbose_name='标题')
    topics=models.ManyToManyField(Topic,related_name="topic_stikers_set")
    # author=models.ForeignKey(settings.AUTH_USER_MODEL,default=get_current_user,on_delete=models.SET_DEFAULT,blank=True,null=True)
    author=models.ForeignKey(StikerUser,related_name="author_stikers_set",on_delete=models.SET_NULL,blank=True, null=True)
    created_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    last_update_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)   # 修改的时候，后期在view强制用timezone更新
    
    stiker=RichTextField(null=True,blank=True,verbose_name="正文")
    stars=models.IntegerField(help_text="赞同人数",null=True,blank=True,verbose_name='stars',default=0)
    unstars=models.IntegerField(help_text="否定人数",null=True,blank=True,verbose_name='unstars',default=0)

    def display_topics(self):
        return ','.join([item.name for item in self.topics.all()])
    display_topics.short_description="话题"

    class Meta:
        verbose_name = '贴文'
        verbose_name_plural = '贴文'

    def __str__(self):
        return str(self.title)                  # 这块要转成str 不然标题为数字或符号的文章会bug，后台删不掉
    