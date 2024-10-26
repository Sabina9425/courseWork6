from django.contrib import admin

from accounts.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_email_verified")
    list_filter = ("email",)
    search_fields = ["email"]
