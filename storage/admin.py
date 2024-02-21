from django.contrib import admin

from .models.files import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'uploaded_at', 'file_name', 'size', 'comment', 'public_link', ]
    list_display_links = ['id', 'file', 'file_name', ]
    list_filter = ['file', 'uploaded_at', 'file_name', 'size', 'comment', ]
    search_fields = ['file', 'uploaded_at', 'file_name', 'size', 'comment', ]
    ordering = ['file', 'size', ]
    # exclude = ('owner', )
    readonly_fields = ['owner', 'uploaded_at', 'modified_at', 'public_link', ]
    list_per_page = 20
