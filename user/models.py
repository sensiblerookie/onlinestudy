from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # 模型类中设置:blank=True,表示代码中创建数据库记录时该字段可传空白(空串,空字符串)
    mobile = models.CharField('手机号', max_length=11, unique=True, null=True)
    fullName = models.CharField('姓名', max_length=64, null=True)  # 用户姓名
    sex = models.CharField('性别', choices=(('0', '女'), ('1', '男'), ('2', '保密')), default='2', max_length=32)
    # userAge = models.IntegerField('年龄', max_length=32, null=True)
    # userSite = models.CharField('地址', max_length=254, null=True)
    userPersona = models.CharField('角色', choices=(('0', '教师'), ('1', '学生')), default='1', max_length=32)
    Class_Data = (('0', '幼儿园'), ('1', '一年级'), ('2', '二年级'), ('3', '三年级'), ('4', '四年级'), ('5', '五年级'), ('6', '六年级'))
    userClass = models.CharField('年级', choices=Class_Data, default='0', max_length=32)
    userPhoto = models.ImageField('用户头像', upload_to='image', blank=True, null=True)
    mod_data = models.DateTimeField('最后修改时间', auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.user.__str__())
