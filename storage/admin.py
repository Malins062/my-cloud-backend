from django.contrib import admin

from .models.files import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name',
                    'uploaded_at',
                    'file_size',
                    'owner',
                    'comment',
                    'file',
                    'public_link', )
    list_display_links = ('file_name', 'uploaded_at', 'file_size', )
    list_filter = ('uploaded_at', 'file_name', 'file_size', 'comment', )
    search_fields = ('uploaded_at', 'file_name', 'file_size', 'comment', )
    ordering = ('file_name', 'file_size', )
    exclude = ('owner', )
    readonly_fields = ('file_size', 'uploaded_at', 'modified_at', 'public_link', 'downloaded_at', )
    list_per_page = 20

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(FileAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['folder'].queryset = Folder.objects.filter(owner=request.user)
    #     return form
    #
    def get_queryset(self, request):
        qs = super(FileAdmin, self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()
