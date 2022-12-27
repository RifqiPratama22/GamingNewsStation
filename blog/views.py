from django.shortcuts import render, redirect
import requests
from blog.models import Kategori, Artikel, Berita
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import request, response
from users.models import Biodata
from users.views import *

from django.contrib.auth.models import User
from .forms import ArtikelForms

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse

from .serializers import ArtikelSerializer

def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False


@login_required
# @user_passes_test(is_operator)
def blog_list(request):
    if request.user.groups.filter(name='Operator').exists():
        request.session['is_operator'] = 'operator'
        print(request.session['is_operator'])
    template_name = 'back/blog_list.html'
    artikel_list = Artikel.objects.all()
    # url ='http://localhost:8000/blog/api/artikel/list/e6f817513acbada95dd64f2b20170bfbdd0828f5df25e32576f283e0b3b3f1a8'
    # #basic auth
    # user_login = "arifnurrahman"
    # user_password = "arifnurrahman"

    # x = requests.get(url, auth=(user_login, user_password))
    # if x.status_code == 200:
    #     print('requests berhasil')
    #     data = x.json()['rows']
    #     for d in data:
    #         print(d['judul'])
    context = {
        'title' : 'List Blog',
        'artikel' :artikel_list
    }
    return render(request, template_name, context)

@login_required
def berita(request):
    template_name = "back/berita.html"
    get_berita = Berita.objects.all()
    context = {
		'berita' : get_berita
	}
    return render(request, template_name, context)

@login_required
def berita_detil(request, title):
    template_name = "back/berita_detil.html"
    get_berita = Berita.objects.get(title=title)
    context = {
		'berita' : get_berita
	}
    return render(request, template_name, context)

@login_required
def sinkron_berita(request):
	url = "https://the-lazy-media-api.vercel.app/api/tech"
	data = requests.get(url).json()
	for d in data:
		cek_berita = Berita.objects.filter(title=d['title'])
		if cek_berita:
			print('data sudah ada')
			c = cek_berita.first()
			c.title=d['title']
			c.save()
		else: 
      		#jika belum ada maka tulis baru kedatabase
			b = Berita.objects.create(
				title = d['title'],
				thumb = d['thumb'],
				author = d['author'],
				tag = d['tag'],
				time = d['time'],
				desc = d['desc'],
				key = d['key']
			)
	return redirect(blog_list)

@login_required
def blog_view(request, id):
    template_name = 'back/blog_view.html'
    artikel_list = Artikel.objects.get(id=id)
    context = {
        'title' : 'News Details',
        'artikel' :artikel_list
    }
    return render(request, template_name, context)
    

@login_required
def blog_add(request):
    template_name = 'back/blog_add.html'
    kategori = Kategori.objects.all()
    if request.method == "POST" :
        forms_artikel = ArtikelForms(request.POST, request.FILES)
        if forms_artikel.is_valid():
            art = forms_artikel.save(commit=False)
            art.nama = request.user
            art.save()
            return redirect(blog_list)
    else:
        forms_artikel = ArtikelForms()
    context = {
        'title' : 'Add News',
        'kategori':kategori,
        'forms_artikel':forms_artikel
    }
    return render(request, template_name, context)

@login_required
def blog_update(request, id):
    template_name = 'back/blog_add.html'
    kategori = Kategori.objects.all()
    get_artikel = Artikel.objects.get(id=id)
    if request.method == "POST" :
        forms_artikel = ArtikelForms(request.POST, request.FILES, instance=get_artikel)
        if forms_artikel.is_valid():
            art = forms_artikel.save(commit=False)
            art.nama = request.user
            art.save()
            return redirect(blog_list)
    else:
        forms_artikel = ArtikelForms(instance=get_artikel)
        
    context = {
        'title' : 'Edit Article',
        'kategori':kategori,
        'get_artikel':get_artikel,
        'forms_artikel':forms_artikel
    }
    return render(request, template_name, context)

@login_required
def blog_delete(request, id):
    artikel = Artikel.objects.get(id=id).delete()
    return redirect(blog_list)



#-------------------API--------------------


def _cek_auth(request, x_api_key):
    # cek auth
    try :
        # Jika tidak error maka except tidak dijalankan
        key = request.user.api.api_key
    except:
        # jika set key error maka jalankan ini
        content = {
            'status': False,
            'messages': 'anda belum melakukan login' 
        }
        return content

    if key != x_api_key:
        content = {
            'status': False,
            'messages': 'x api key tidak sama'
        }
        return content

    return True
    #end cek auth


@api_view(['GET'])
def artikel_list(request, x_api_key):
    cek = _cek_auth(request, x_api_key)
    if cek != True:
        return Response(cek)

    list = Artikel.objects.all()
    jumlah_artikel = list.count()
    serializer = ArtikelSerializer(list, many=True)
    content = {
        'status': True,
        'records': jumlah_artikel,
        'rows': serializer.data
    }
    return Response(content)


@api_view(['POST',])
def artikel_post(request, x_api_key):
    # untuk auth
    cek = _cek_auth(request, x_api_key)
    if cek != True:
        return Response(cek)

    
    if request.method == 'POST':
        serializer = ArtikelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'status': status.HTTP_201_CREATED,
                'messages': 'berhasil membuat data'
            }
            return Response(content)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {
            'status':status.HTTP_405_METHOD_NOT_ALLOWED,
            'messages':'method tidak ditemukan'
        }
        return Response(content)


@api_view(['GET', 'PUT', 'DELETE'])
def artikel_detail(request, pk, x_api_key):
    # cek auth
    cek = _cek_auth(request, x_api_key)
    if cek != True:
        return Response(cek)
    #end cek auth
    
    try:
        artikel = Artikel.objects.get(pk=pk)
    except Artikel.DoesNotExist:
        content = {
            'status':status.HTTP_404_NOT_FOUND,
            'messages': 'artikel tidak ada'
        }
        return Response(content, status.HTTP_404_NOT_FOUND)

    #berhasil
    if request.method == 'GET':
        serializer = ArtikelSerializer(artikel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArtikelSerializer(artikel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
                'status': status.HTTP_202_ACCEPTED,
                'messages':'berhasil diupdate',
                'rows': serializer.data
            }
            return Response(content, status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        artikel.delete()
        content = {
            'status' : status.HTTP_204_NO_CONTENT,
            'messages': 'berhasil didelete'
        }
        return Response(content, status=status.HTTP_204_NO_CONTENT)