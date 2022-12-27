from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Kategori(models.Model):
    nama = models.CharField(max_length=40)
    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural ="Kategori"
class Artikel(models.Model):
    nama = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    judul = models.TextField(max_length=100)
    body = RichTextUploadingField(blank=True, null=True,
                                      config_name='special',
                                      external_plugin_resources=[(
                                          'youtube',
                                          '/static/ckeditor_plugins/youtube/youtube/',
                                          'plugin.js',
                                          )]
    )
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='artikel/thumbnail/', blank=True, null=True)


    def __str__(self):
        return str(self.nama)

    def ImgUrl(self):
        if self.thumbnail == '' or self.thumbnail == None:
            gambar = 'http://localhost:8000/static/default_thumbnail.jpg'
        else:
            gambar = self.thumbnail.url
        return gambar

    class Meta:
        verbose_name_plural ="Artikel"


class Berita(models.Model):
    title = models.CharField(max_length=255, unique=True)
    thumb = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    time = models.CharField(max_length=50, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    key = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title