from django.db import models
from django.shortcuts import reverse
# Create your models here.
import datetime

from ckeditor.fields import RichTextField

class Genre(models.Model):
    '''
    存放书籍的类型
    '''
    name=models.CharField(max_length=200,help_text="输入书籍的类型(比如，python，linux，技术，非技术等等)",verbose_name="类别名称")
    class Meta:
        verbose_name_plural="类别"
        verbose_name="类别"

    def __str__(self):
        return self.name

class Author(models.Model):
    name=models.CharField(max_length=100,verbose_name='名字')
    data_birth=models.DateField(null=True,blank=True,verbose_name="出生于")
    data_death=models.DateField('Died',null=True,blank=True)
    
    class Meta:
        verbose_name_plural="作者"
        verbose_name="作者"
    
    def get_absolute_url(self):
        return reverse('author_detail',args=[str(self.id)])

    def __str__(self):
        return '{}'.format(self.name)

    def birth_year(self):
        # return datetime.datetime.strftime(self.data_birth,'%Y-%m-%d')
        if self.data_birth is not None:
            return datetime.datetime.strftime(self.data_birth,'%Y')
        else:
            return '未知'
    birth_year.short_description="生于"

    def display_books(self):
        return  '《'+'》,《 '.join([book.title for book in self.book_author_set.all()[:5]])+'》'
    display_books.short_description="已收录作品"

class Book(models.Model):
    title=models.CharField(max_length=200,verbose_name='标题')
    author=models.ManyToManyField(Author,related_name="book_author_set")
    short_summary=models.CharField(help_text="丛书短简介（library页面会有显示，注意字数）：", max_length=100,null=True,blank=True)
    summary=RichTextField(help_text="丛书简介：",null=True,blank=True,verbose_name='简述')
    isbn=models.CharField(max_length=13,help_text="书籍ISBN编号",null=True,blank=True,verbose_name="ISBN编号")
    genre=models.ManyToManyField(Genre,related_name="book_genre_set")
    # ebookfile=models.FileField(upload_to='static/pic/upload')
    stars=models.IntegerField(help_text="喜欢人数",null=True,blank=True,verbose_name='stars')
    
    class Meta:
        verbose_name_plural="书籍"
        verbose_name="书籍"
     
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail',args=[str(self.id)])         # 考虑引入一个唯一id

    def display_genre(self):
        return ','.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = '类别'

    def display_author(self):
        return ','.join([author.name for author in self.author.all()[:3]])
    display_author.short_description='作者'
# 电子书 不需要考虑 实体图书管理的借阅状态和书籍实例问题
# import uuid # Required for unique book instances

# class BookInstance(models.Model):
#     """
#     Model representing a specific copy of a book (i.e. that can be borrowed from the library).
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
#     book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
#     imprint = models.CharField(max_length=200)
#     due_back = models.DateField(null=True, blank=True)

#     LOAN_STATUS = (
#         ('m', 'Maintenance'),
#         ('o', 'On loan'),
#         ('a', 'Available'),
#         ('r', 'Reserved'),
#     )

#     status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

#     class Meta:
#         ordering = ["due_back"]
        

#     def __str__(self):
#         """
#         String for representing the Model object
#         """
#         return '%s (%s)' % (self.id,self.book.title)