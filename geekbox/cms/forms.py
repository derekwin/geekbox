from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models.Users  import StikerUser
from .models.Stikers import Stiker
from .models.Comments import Comment,Reply

# from pagedown.widgets import PagedownWidget             # pagedown 编辑器 弃用
from django.forms import widgets
# 注册时，注册用户的表单
class CreateUser(UserCreationForm):
    class Meta:
        model = StikerUser
        fields = ['username','Icon','email','first_name','last_name','Gender','Introduce_short','Introduce','InvitedCode','password1','password2']


# 发帖的表单
class CreateStiker(forms.ModelForm):
    # stiker=forms.CharField(widget=PagedownWidget())
    # stiker=forms.CharField(widget=forms.Textarea(attrs={
    #     'style': 'height: 200px;width:278px',
    #     'placeholder':'请输入内容',
    #     }))
    # 换ckeditor后 ，首页取消直接创建话题的功能，首页的创建直接重定向一个create页面，首页滑动侧栏有bug，导致无法使用模态框
    # topics=forms.CheckboxSelectMultiple
    class Meta:
        model=Stiker
        fields = ['title','topics','stiker']
        
# 评论的表单
class CreateComment(forms.ModelForm):
    # comment=forms.CharField(widget=PagedownWidget())
    class Meta:
        model=Comment
        fields = ['comment']

# 回复的表单
class CreateReply(forms.ModelForm):
    # reply=forms.CharField(widget=PagedownWidget())
    class Meta:
        model=Reply
        fields = ['reply']

# 回复嵌入markdown https://github.com/timmyomahony/django-pagedown