from django.urls import path
from blog.views import *
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from blog.views import berita, berita_detil, sinkron_berita

urlpatterns = [
    path('list',blog_list, name='blog_list'),
    path('add',blog_add, name='blog_add'),
    path('update/<int:id>',blog_update, name='blog_update'),
    path('view/<int:id>',blog_view, name='blog_view'),
    path('delete/<int:id>',blog_delete, name='blog_delete'),

    #api
    path('api/artikel/list/<str:x_api_key>',artikel_list, name='artikel_list'),
    path('api/artikel/post/<str:x_api_key>',artikel_post, name='artikel_post'),
    path('api/artikel/detail/<int:pk>/<str:x_api_key>',artikel_detail, name='artikel_detail'),

    path('', berita, name='berita'),
    path('sinkron-berita', sinkron_berita, name='sinkron_berita'),
    path('detil/<str:title>', berita_detil, name='berita_detil'),
]

urlpatterns = format_suffix_patterns(urlpatterns)