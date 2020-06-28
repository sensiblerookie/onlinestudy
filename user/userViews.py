from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .myForms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required


#
# # Create your views here.
#
# def login(request):
#     if request.session.get('is_login', None):
#         return redirect('/home/')
#
#     if request.POST:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if username == '':
#             return render(request, 'login.html', {'error': '账号不能为空'})
#         else:
#             if password == '':
#                 return render(request, 'login.html', {'error': '密码不能为空'})
#             else:
#                 if not User.objects.filter(username__exact=username):
#                     return render(request, 'login.html', {'error': '该用户不存在，请先注册'})
#                 else:
#                     user = auth.authenticate(username=username, password=password)
#                     if user is not None and user.is_active:
#                         auth.login(request, user)
#                         fullname = UserProfile.objects.get(user_id=user.id).fullName
#                         if fullname is None:
#                             request.session['user'] = username
#                         else:
#                             request.session['user'] = fullname
#                         request.session['is_login'] = True
#                         request.session['_auth_user_id'] = user.id
#                         response = HttpResponseRedirect('/home/')
#                         return response
#                     else:
#                         return render(request, 'login.html', {'error': '账号和密码不匹配'})
#
#     #     # if request.POST:
#     #     #     username = request.POST.get('username')
#     #     #     password = request.POST.get('password')
#     #     #     print(username)
#     #     #     print(password)
#     #     #     if username == '' and password == '':
#     #     #         return render(request, 'login.html', {'error': '昵称或密码不能为空'})
#     #     #     else:
#     #     #         user = User.objects.get(userName=username)
#     #     #         print(user.fullName)
#     #     #         if user is not None:
#     #     #             if user.password == password:
#     #     #                 request.session['user'] = user.fullName
#     #     #                 request.session['_auth_user_id'] = user.id
#     #     #                 request.session['is_login'] = True
#     #     #                 # response = HttpResponseRedirect('/home/')
#     #     #                 # return response
#     #     #                 return redirect('/home/')
#     #     #             else:
#     #     #                 return render(request, 'login.html', {'error': '密码不正确'})
#     #     #         else:
#     #     #             return render(request, 'login.html', {'error': '用户不存在'})
#     #
#     return render(request, 'login.html')


#
#
# def logout(request):
#     auth.logout(request)
#     return render(request, 'login.html')
#
#
# def register(request):
#     if request.POST:
#         username = request.POST.get('userName')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         fullname = request.POST.get('fullName')
#         sex = request.POST.get('Sex')
#         mobile = request.POST.get('mobile')
#         email = request.POST.get('email')
#         if username == '' or password1 == '' or password2 == '' or fullname == '':
#             return render(request, "register.html", {"error": '必填项不能为空'})
#         else:
#             if User.objects.filter(username=username):
#                 return render(request, "register.html", {"error": '昵称已存在'})
#             else:
#                 if password1 != password2:
#                     return render(request, "register.html", {"error": '两次密码不一致'})
#                 else:
#                     user = User.objects.create_user(username=username, password=password1, email=email)
#
#                     # 如果直接使用objects.create()方法后不需要使用save()
#                     user_profile = UserProfile(user=user, fullName=fullname, sex=sex, mobile=mobile)
#                     user_profile.save()
#
#                     return HttpResponseRedirect('/login/', {'success': '注册成功！请返回登录'})
#     return render(request, 'register.html')


#
#
# def personal(request):
#     pass
#     return render(request, 'personal.html')


# Create your views here.

@login_required
# def profile(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     return render(request, 'profile.html', {'user': user})
def profile(request):
    # form = ProfileForm()
    user_id = request.session.get('_auth_user_id')
    user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user_id=user_id)

    print(user_profile.sex)
    """判断性别"""
    if int(user_profile.sex) == 0:
        sex = user_profile.get_sex_display() + ' ♀'
    elif int(user_profile.sex) == 1:
        sex = user_profile.get_sex_display() + ' ♂'
    else:
        sex = user_profile.get_sex_display()
    """判断邮箱"""

    """判断手机号"""
    if user_profile.mobile is None:
        mobile = '无'
    else:
        mobile = user_profile.mobile[0:3] + '****' + user_profile.mobile[-4:]
    print('邮箱的值', type(user.email), len(user.email))
    # return render(request, 'profile.html', {'user': user_profile, 'sex': user.get_sex_display()})
    return render(request, 'profile.html',
                  {'user': user,
                   'user_profile': user_profile,
                   'sex': sex,
                   'email': len(user.email),
                   'mobile': mobile,
                   'userPersona': user_profile.get_userPersona_display(),
                   'userClass': user_profile.get_userClass_display()})


@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)

    return render(request, 'users/profile_update.html', {'form': form, 'user': user})


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            fullname = form.cleaned_data['fullname']
            sex = form.cleaned_data['sex']
            mobile = form.cleaned_data['mobile']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password, email=email)

            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user, fullName=fullname, sex=sex, mobile=mobile)
            user_profile.save()

            return HttpResponseRedirect("/login/")
        else:
            error_msg = form.errors
            return render(request, 'register.html', {'form': form, 'error': error_msg})
    return render(request, 'register.html', {'form': form})


#
def login(request):
    if request.session.get('is_login', None):
        return redirect('/home/')
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                fullname = UserProfile.objects.get(user_id=user.id).fullName
                if fullname is None:
                    request.session['user'] = username
                else:
                    request.session['user'] = fullname
                request.session['is_login'] = True
                request.session['_auth_user_id'] = user.id
                request.session['sex'] = UserProfile.objects.get(user_id=user.id).sex
                request.session['persona'] = UserProfile.objects.get(user_id=user.id).userPersona
                if user.is_staff:
                    return render(request, 'profile.html', {'form': form})
                else:
                    return HttpResponseRedirect('/home/')
            else:
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/accounts/login/')

            else:
                return render(request, 'users/pwd_change.html', {'form': form,
                                                                 'user': user,
                                                                 'message': 'Old password is wrong Try again'})
    else:
        form = PwdChangeForm()

    return render(request, 'users/pwd_change.html', {'form': form, 'user': user})
