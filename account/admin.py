from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

UserAdmin.fieldsets[2][1]['fields'] = (
    "is_active",
    "is_staff",
    "is_superuser",
    "is_author",
    "special_user",
    "groups",
    "user_permissions",
),

UserAdmin.list_display += ("is_author", "is_special_user")
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Form_Registeration)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('jrpublish', 'user')
admin.site.register(models.Reserve, ReserveAdmin)
