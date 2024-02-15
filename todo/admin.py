from django.contrib import admin
from .models import Todo,User_info


@admin.register(Todo,User_info)
class PersonAdmin(admin.ModelAdmin):
    pass

