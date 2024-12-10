from django.contrib import admin
from . import models
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	

# Register your models here.

# admin header site
admin.site.site_header = "سایت اطلاع رسانی دبیرستان دوره اول « شهیدان احسانی »"

def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status = "p")
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status = "d")
    if rows_updated == 1:
        message_bit = "پیش‌نویس شد."
    else:
        message_bit = "پیش‌نویس شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_updated, message_bit))
make_draft.short_description = "پیش‌نویس کردن مقالات انتخاب شده"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'slug', 'name', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('slug', 'name')
    prepopulated_fields = {'slug' : ('englishName',)}

admin.site.register(models.Category, CategoryAdmin)


class ArticleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('slug', 'title', 'thumbnail_tag', 'jpublish', 'is_special', 'status', 'categoryToStr', "author")
    list_filter = ('publish', 'status', 'author')
    search_fields = ('slug', 'title', 'description')
    prepopulated_fields = {'slug' : ('englishTitle',)}
    ordering = ('-updated', '-created')
    actions = [make_published, make_draft]


admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.IPAddress)