from django.db import models

# Create your models here.

class wiki_instance(models.Model):
    
    name=models.CharField(max_length=50,help_text="markdown文档名")

    markdown=models.TextField(help_text="文档内容，仅支持markdown，导入markdown文件，前台自动渲染")