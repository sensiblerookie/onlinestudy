# Generated by Django 3.0.7 on 2020-06-28 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, null=True, unique=True, verbose_name='手机号')),
                ('fullName', models.CharField(max_length=64, null=True, verbose_name='姓名')),
                ('sex', models.CharField(choices=[('0', '女'), ('1', '男'), ('2', '保密')], default='2', max_length=32, verbose_name='性别')),
                ('userPersona', models.CharField(choices=[('0', '教师'), ('1', '学生')], default='1', max_length=32, verbose_name='角色')),
                ('userClass', models.CharField(choices=[('0', '幼儿园'), ('1', '一年级'), ('2', '二年级'), ('3', '三年级'), ('4', '四年级'), ('5', '五年级'), ('6', '六年级')], default='0', max_length=32, verbose_name='年级')),
                ('userPhoto', models.ImageField(blank=True, null=True, upload_to='image', verbose_name='用户头像')),
                ('mod_data', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
    ]
