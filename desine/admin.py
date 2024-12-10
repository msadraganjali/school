from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	

# Register your models here.
class ImageAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    pass
admin.site.register(models.Image, ImageAdmin)