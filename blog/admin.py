from django.contrib import admin
from blog.models import *
# Register your models here
admin.site.register(Kategori)


class ArtikelAdmin(admin.ModelAdmin):
    list_display = ['nama','judul','body','date']
admin.site.register(Artikel, ArtikelAdmin)
