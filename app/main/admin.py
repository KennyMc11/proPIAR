from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Информация о заявке', {
            'fields': ('name', 'phone')
        }),
        ('Данные системы', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
