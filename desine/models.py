from django.db import models
from django.utils import timezone
from extensions.utils import jalali_converter

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=100)
    img  = models.ImageField(upload_to='ui/')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "عکس ها"