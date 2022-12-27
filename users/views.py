from django.http import request
# from django.http import HttpResponse
# from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import Biodata
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import UserForms, BiodataForms


def is_operator(user):
    if user.groups.filter(name='Operator').exists():
        return True
    else:
        return False

@login_required
@user_passes_test(is_operator)
def users(request):
    template_name = 'back/list_users.html'
    list_users = User.objects.all()
    context = {
        'title' : 'List Users',
        'list_users':list_users
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator)
def users_view(request, id):
    template_name = 'back/users_view.html'
    try :
        user_info = User.objects.get(id=id)
        biodataku = Biodata.objects.get(user=user_info)
    except :
        return redirect(users)
    context = {
        'title' : 'Details User',
        'user_info': user_info,
        'biodataku': biodataku,
    }
    return render(request, template_name, context)

@login_required
@user_passes_test(is_operator)
def users_update(request, id):
    template_name = 'back/users_update.html'
    try :
        user_info = User.objects.get(id=id)
        biodataku = Biodata.objects.get(user=user_info)
    except :
        return redirect(users)

    if request.method == "POST":
        forms_user = UserForms(request.POST, instance=user_info)
        forms_biodata = BiodataForms(request.POST, instance=biodataku)
        if forms_user.is_valid() and forms_biodata.is_valid():
            test = forms_user.save(commit=False)
            test.is_active = True
            test.save()
            forms_biodata.save()
            print('tetsing form')
            return redirect(users)
    else:
        forms_user = UserForms(instance=user_info)
        forms_biodata = BiodataForms(instance=biodataku)
    context = {
        'title' : 'Update Users',
        'user_info': user_info,
        'biodataku': biodataku,

        'forms_user':forms_user,
        'forms_biodata':forms_biodata
    }
    return render(request, template_name, context)


@login_required
@user_passes_test(is_operator)
def users_delete(request, id):
    try:
        User.objects.get(id=id).delete()
    except:
        pass
    return redirect('users')


def registrasi_add(request):
    template_name = 'account/register_add.html'
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
            return redirect(users)
        except:pass

    context = {
        'title' : 'Add Form Registrasi'
    }
    return render(request, template_name, context)


# def registrasi_update(request, id):
#     template_name = 'account/register_add.html'
#     biodata = Biodata.objects.all()
#     get_users = User.objects.get(id=id)
#     if request.method == "POST" :
        
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         nama_depan = request.POST.get('nama_depan')
#         nama_belakang = request.POST.get('nama_belakang')
#         email = request.POST.get('email')
#         alamat = request.POST.get('alamat')
#         telp = request.POST.get('telp')

#         #Panggil kategori
    
#         #Simpan artikel karena ada relasi ke tabel kategori
#         get_users.username = username
#         get_users.password = password
#         get_users.first_name = nama_depan
#         get_users.last_name = nama_belakang
#         get_users.email = email
#         get_users.alamat = alamat
#         get_users.telp = telp
#         get_users.save()
#         return redirect(list_users)
#     context = {
#         'title' : 'ini adalah halaman update user',
#         'biodata':biodata,
#         'get_users':get_users
#     }
#     return render(request, template_name, context)

# def users_delete(request, id):
#     user = User.objects.get(id=id).delete()
#     return redirect(list_users)