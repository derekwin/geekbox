from django.db import models
from .Stikers import Stiker
from .Users import StikerUser

from mptt.models import MPTTModel,TreeForeignKey
from ckeditor.fields import RichTextField
# 采用评论表和回复表拆分的形式
# 回复表挂在评论表下面
# 评论表挂在贴文表下

class Comment(models.Model):
    created_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    stiker=models.ForeignKey(Stiker,related_name='stiker_comments_set',on_delete=models.CASCADE,null=True,blank=True)
    # 级联删除 ，贴删去之后，评论也都删除
    author=models.ForeignKey(StikerUser,related_name='author_comments_set',on_delete=models.SET_NULL,null=True,blank=True)
    # 作者删除后，作者置于NUll，评论不删除
    comment=RichTextField()
    stars=models.IntegerField(help_text="赞同人数",null=True,blank=True,verbose_name='stars',default=0)
    unstars=models.IntegerField(help_text="否定人数",null=True,blank=True,verbose_name='unstars',default=0)

    class Meta:
        verbose_name='评论'
        verbose_name_plural="评论"

    def __str__(self):
        # return str(self.stiker.stiker[:30])
       return str(self.id) 
    

class Reply(MPTTModel):
    created_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    comment=models.ForeignKey(Comment,related_name='comment_replys_set',on_delete=models.CASCADE,null=True,blank=True)
    author=models.ForeignKey(StikerUser,related_name='author_replys_set',on_delete=models.SET_NULL,null=True,blank=True)
    reply=RichTextField()
    stars=models.IntegerField(help_text="赞同人数",null=True,blank=True,verbose_name='stars',default=0)
    unstars=models.IntegerField(help_text="否定人数",null=True,blank=True,verbose_name='unstars',default=0)
    parent=TreeForeignKey('self',related_name='children',on_delete=models.SET_NULL,null=True,blank=True)

    # 设计有点冗余

    class MPTTMeta:
        verbose_name='回复'
        verbose_name_plural="回复"
        order_insertion_by=['created_time']

    def __str__(self):
        # return str(self.comment[:20])
        return str(self.id)                          # 自己生成的回复 会自动绑定id 但是后台测试的时候 return的字符串 会导致回复无法保存
    



