from django import forms
from django.contrib.auth.models import User
import re

from .models import UserProfile


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")  # 检查邮箱是否合法
    return re.match(pattern, email)


def mobile_check(mobile):
    pattern = re.compile(r"^1[35678]\d{9}$")  # 检查手机号是否合法
    return re.match(pattern, mobile)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='昵称(必填)',
                               max_length=64,
                               widget=forms.TextInput(
                                   attrs={'class': "form-control", 'placeholder': "输入昵称"}
                               ))
    password1 = forms.CharField(label='密码(必填)',
                                widget=forms.PasswordInput(
                                    attrs={'class': "form-control", 'placeholder': "输入密码"}
                                ))
    password2 = forms.CharField(label='确认密码(必填)',
                                widget=forms.PasswordInput(
                                    attrs={'class': "form-control", 'placeholder': "输入确认密码"}
                                ))
    fullname = forms.CharField(label='姓名(必填)',
                               max_length=50,
                               widget=forms.TextInput(
                                   attrs={'class': "form-control", 'placeholder': "输入姓名"}
                               ))
    sex = forms.ChoiceField(label='性别(必填)',
                            choices=((0, '女'), (1, '男'), (2, '保密')),
                            initial=2,
                            widget=forms.Select(
                                attrs={'class': "form-control"}
                            ))
    userPersona = forms.ChoiceField(label='角色(必填)',
                                    choices=((0, '教师'), (1, '学生')),
                                    initial=1,
                                    widget=forms.Select(
                                        attrs={'class': "form-control"}
                                    ))
    userClass = forms.ChoiceField(label='年级(必填)',
                                  choices=(
                                      (0, '幼儿园'), (1, '一年级'), (2, '二年级'), (3, '三年级'), (4, '四年级'), (5, '五年级'),
                                      (6, '六年级'),),
                                  initial=0,
                                  widget=forms.Select(
                                      attrs={'class': "form-control"}
                                  ))

    mobile = forms.IntegerField(label='电话',
                                required=False,
                                widget=forms.NumberInput(
                                    attrs={'class': "form-control", 'placeholder': "输入手机号"}
                                ))
    email = forms.EmailField(label='邮箱',
                             max_length=256,
                             required=False,
                             widget=forms.EmailInput(
                                 attrs={'class': "form-control", 'placeholder': "输入邮箱"}
                             ))

    # user clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("你的昵称小于3位")
        elif len(username) > 20:
            raise forms.ValidationError("你的昵称大于20位")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError('此昵称已存在，请重新输入')
        return username

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile_check(str(mobile)):
            filter_result = UserProfile.objects.filter(mobile__exact=mobile)
            if len(filter_result) > 0:
                raise forms.ValidationError('此手机号已注册，请重新输入')
        # else:
        #     raise forms.ValidationError('手机号格式错误，请重新输入')
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("此邮箱已注册，请重新输入")
        # else:
        #     raise forms.ValidationError("请输入有效的邮箱")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise forms.ValidationError("密码长度不能小于3位")
        elif len(password1) > 20:
            raise forms.ValidationError("密码长度不能大于20位入")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次密码不一致，请重新输入')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='昵称', max_length=50,
                               widget=forms.TextInput(
                                   attrs={'class': "form-control", 'placeholder': "输入账号"}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                   attrs={'class': "form-control", 'placeholder': "输入密码"}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # password = self.cleaned_data.get('password')
        if mobile_check(username):
            filter_result = UserProfile.objects.filter(mobile__exact=username)
            if not filter_result:
                raise forms.ValidationError('该电话未注册，请先注册')
            # else:
            #     filter_result = User.objects.filter(mobile__exact=username).filter(password__exact=password)
            #     if not filter_result:
            #         raise forms.ValidationError('密码错误，请重新输入')
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError('该昵称不存在，请先注册')
            # else:
            #     filter_result = User.objects.filter(mobile__exact=username).filter(password__exact=password)
            #     if not filter_result:
            #         raise forms.ValidationError('密码错误，请重新输入')
        return username

    # 有bug
    # def clean_password(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     filter_result = User.objects.filter(username__exact=username).filter(password__exact=password)
    #     if filter_result:
    #         raise forms.ValidationError('密码错误，请输入正确的密码')
    #     return password


class ProfileForm(forms.Form):
    username = forms.CharField(label='昵称(必填)',
                               max_length=64,
                               widget=forms.TextInput(
                                   attrs={'class': "form-control", 'value': "输入昵称"}))
    fullname = forms.CharField(label='First Name',
                               max_length=50,
                               required=False,
                               widget=forms.TextInput(
                                   attrs={'class': "form-control", 'value': "输入昵称"}))
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='Organization', max_length=50, required=False)
    telephone = forms.CharField(label='Telephone', max_length=50, required=False)


class PwdChangeForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)

    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch Please enter again")

        return password2


# class TitleAddForm(forms.Form):
#     Course = forms.CharField(label='科目',
#                              choices=(('0', '语文'), ('1', '数学'), ('2', '英语'), ('3', '品德与生活'), ('4', '科学')),
#                              initial='---',
#                              widget=forms.Select(
#                                  attrs={'class': "form-control"}
#                              ))
#     titleType = forms.CharField(label='题目类型',
#                                 choices=(('0', '计算题'), ('1', '填空题'), ('2', '选择题'), ('3', '判断题'), ('4', '应用题'),
#                                          ('5', '奥数题'), ('6', '阅读题'), ('7', '翻译题'), ('8', '写作题')),
#                                 initial='---',
#                                 widget=forms.Select(
#                                     attrs={'class': "form-control"}
#                                 ))
#     applyClass = forms.ChoiceField(label='年级',
#                                    choices=((0, '幼儿园'), (1, '一年级'), (2, '二年级'), (3, '三年级'), (4, '四年级'), (5, '五年级'),
#                                             (6, '六年级')),
#                                    initial='---',
#                                    widget=forms.Select(
#                                        attrs={'class': "form-control"}
#                                    ))
