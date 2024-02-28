import os
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from django.db.models.signals import pre_delete

from config.settings import FILE_STORAGE_ROOT


# Path to file storage
files_storage: FileSystemStorage = FileSystemStorage(location=os.path.join(FILE_STORAGE_ROOT))

# User
User = get_user_model()


# Path to user files
def get_upload_path(instance, file_name):
    return os.path.join(f'user_{instance.owner.id}', file_name)


class File(models.Model):
    owner = models.ForeignKey(verbose_name='Владелец', to=User, on_delete=models.CASCADE, )
    file = models.FileField(verbose_name='Файл',
                            upload_to=get_upload_path,
                            storage=files_storage, )
    file_name = models.CharField(verbose_name='Имя файла', max_length=255,  editable=False, null=True, blank=True, )
    file_size = models.PositiveIntegerField(verbose_name='Размер файла', editable=False, null=True, blank=True, )
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True, )

    uploaded_at = models.DateTimeField(verbose_name='Дата загрузки', null=True, blank=True, default=None, )
    modified_at = models.DateTimeField(verbose_name='Дата изменения', null=True, blank=True, default=None, )

    public_link = models.CharField(verbose_name='Ссылка для скачивания', max_length=50, null=True, blank=True, )
    downloaded_at = models.DateTimeField(verbose_name='Дата скачивания', null=True, blank=True, default=None, )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-uploaded_at']

    def save(self, *args, **kwargs):
        if not self.pk and not self.uploaded_at:
            self.uploaded_at = timezone.now()
        self.modified_at = timezone.now()

        if not self.file_name and self.file:
            self.file_name = os.path.basename(self.file.name)

        if self.file:
            self.file_size = self.file.size

        return super(File, self).save(*args, **kwargs)

    def __str__(self):
        return self.file.name


@receiver(pre_delete, sender=User)
def delete_files(sender, instance, **kwargs):
    user = instance
    files = File.objects.filter(owner=user)
    for file in files:
        file_path = file.file.path
        if os.path.exists(file_path):
            os.remove(file_path)
