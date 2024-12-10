from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from account.models import User
from extensions.utils import jalali_converter
# Create your models here.

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status = "p")
class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status = True)

class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name="children", verbose_name="زیردسته")
    name = models.CharField(max_length=255, verbose_name="نام دسته‌بندی")
    englishName = models.CharField(max_length=255, verbose_name="عنوان انگلیسی دسته‌بندی")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="آدرس دسته‌بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")
    
    objects = CategoryManager()


    class Meta:
        ordering = ['parent__id','-position']
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
    
    def __str__(self):
        return self.name


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آی‌پی")

class Article(models.Model):
    
    ARTICLE_STATUS_CHOICES = (
        ('d', 'پیش‌نویس'),
        ('p', 'منتشر شده'),
        ('i', 'در انظار تایید'),
        ('b', 'برگشت داده شده'),
    )
    
    author = models.ForeignKey(User, null=True, on_delete = models.SET_NULL, related_name="articles", verbose_name="نویسنده")
    title = models.CharField(max_length=255, verbose_name="عنوان مقاله")
    englishTitle = models.CharField(max_length=255, verbose_name="عنوان انگلیسی مقاله", null=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="آدرس مقاله")
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی', related_name="articles")
    description = models.TextField(verbose_name="محتوا")
    thumbnail = models.ImageField(upload_to='images/', verbose_name="تصویر مقاله")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS_CHOICES, verbose_name="وضعیت")
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه است؟")
    hits = models.ManyToManyField(IPAddress, through="ArticleHit", blank=True, related_name="hits", verbose_name="بازدیدها")

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("auth:home")
    
    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width='160px' height='90px' style='border-radius: 5px' src='{}'></img>".format(self.thumbnail.url))
        # return format_html("<img width=100 height=75 style='border-radius: 5px' src='{}'></img>".format(self.thumbnail.url))
    thumbnail_tag.short_description = "تصویر مقاله"

    def categoryToStr(self):
        return ", ".join([category.name for category in self.category.active()])
    categoryToStr.short_description = "دسته‌بندی‌"
    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    objects = ArticleManager()
    
class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)