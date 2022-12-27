from django.contrib.auth.models import User
from users.models import Biodata
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from blog.models import Kategori, Artikel, Berita
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    template_name = 'front/index.html'
    artikel_list = Artikel.objects.all()
    kategori = Kategori.objects.all()
    get_berita = Berita.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(artikel_list, 3)
    try:
        artikel_list = paginator.page(page)
    except PageNotAnInteger:
        artikel_list = paginator.page(1)
    except EmptyPage:
        artikel_list = paginator.page(paginator.num_pages)
    context = {
        'title' : 'Gaming News Station',
        'artikel' :artikel_list,
        'berita' : get_berita,
        'kategori' :kategori,
    }
    return render(request, template_name, context)

def artikel_filter(request, nama):
    template_name = 'front/index.html'
    kategori = Kategori.objects.all()
    artikel_list = Artikel.objects.filter(kategori__nama=nama)
    context = {
        'title' : 'Kategori',
        'artikel' :artikel_list,
        'kategori' :kategori,
    }
    return render(request, template_name, context)

def detail_artikel(request, id):
    template_name = 'front/detail_artikel.html'
    artikel_list = Artikel.objects.get(id=id)
    context = {
        'title' : 'Details Article',
        'artikel' :artikel_list
    }
    return render(request, template_name, context)

def detail_berita(request, title):
    template_name = "front/detail_berita.html"
    get_berita = Berita.objects.get(title=title)
    context = {
		'berita' : get_berita
	}
    return render(request, template_name, context)

def about(request):
    template_name = 'front/about.html'
    context = {
        'title' : 'About'
    }
    return render(request, template_name, context)

def login(request):
    if request.user.is_authenticated:
        print('sudah login')
        return redirect('index')
    template_name = 'account/login.html'
    if request.method == "POST":
        username = request.POST.get ('username')
        password = request.POST.get ('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #username ada
            print('username anda benar')
            auth_login(request, user)
            return redirect('index')
        else:
            #username tidak ada
            print("username anda salah")
    context = {
        'title' : 'Form Login'
    }
    return render(request, template_name, context)

def logout_view(request):
    logout(request)
    return redirect('index')

def registrasi(request):
    template_name = 'account/register.html'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nama_depan = request.POST.get('nama_depan')
        nama_belakang = request.POST.get('nama_belakang')
        email = request.POST.get('email')
        alamat = request.POST.get('alamat')
        telp = request.POST.get('telp')
        try:
            with transaction.atomic():
                User.objects.create(
                    username = username,
                    password = make_password(password),
                    first_name = nama_depan,
                    last_name = nama_belakang,
                    email = email
                )
                get_user = User.objects.get(username = username)
                Biodata.objects.create(
                    user = get_user,
                    alamat = alamat,
                    telp = telp,
                )
            return redirect(index)
        except:pass

    context = {
        'title' : 'Form Registrasi'
    }
    return render(request, template_name, context)