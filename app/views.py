import json

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import random
import time
import ast
import math
import datetime
from app.models import TitleStore, SelectTitleInfo, AnswerInfo
from user.models import UserProfile
from app import models
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from django.contrib.auth.decorators import login_required

# from user.myForms import TitleAddForm

# 使用数据mysql
'''将结果页的内容生成图片'''


def new_image(width, height, color):  # 生成空的图片模板
    img = Image.new('RGBA', (int(width), int(height)), color)
    img.save('./static/image/app/test.png')


def synthesis_image(mother_img, son_img, son_img1, save_img, coordinate=None):
    """
    :param mother_img: 根据需求图片高度，自动生成纯色母图
    :param son_img: 子图
    :param save_img: 保存图片名
    :param coordinate: 子图在母图的坐标
    :return:
    """
    # 将图片赋值,方便后面的代码调用
    M_Img = Image.open(mother_img)
    S_Img = Image.open(son_img)
    S_Img1 = Image.open(son_img1)
    factor = 2  # 子图缩小的倍数1代表不变，2就代表原来的一半

    # 给图片指定色彩显示格式
    M_Img = M_Img.convert("RGBA")  # CMYK/RGBA 转换颜色格式（CMYK用于打印机的色彩，RGBA用于显示器的色彩）

    # 获取图片的尺寸
    M_Img_w, M_Img_h = M_Img.size  # 获取被放图片的大小（母图）
    print("母图尺寸：", M_Img.size)
    S_Img_w, S_Img_h = S_Img.size  # 获取小图的大小（子图）
    print("子图尺寸：", S_Img.size)
    S_Img_w1, S_Img_h1 = S_Img1.size  # 获取小图的大小（子图）
    print("子图尺寸：", S_Img1.size)

    size_w = int(S_Img_w / factor)
    size_w1 = int(S_Img_w1 / factor)
    size_h = int(S_Img_h / factor)
    size_h1 = int(S_Img_h1 / factor)

    # 防止子图尺寸大于母图
    if S_Img_w > size_w:
        S_Img_w = size_w
    if S_Img_h > size_h:
        S_Img_h = size_h
    if S_Img_w1 > size_w1:
        S_Img_w1 = size_w1
    if S_Img_h1 > size_h1:
        S_Img_h1 = size_h1

    # # 重新设置子图的尺寸
    icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    icon1 = S_Img1.resize((S_Img_w1, S_Img_h1), Image.ANTIALIAS)
    w = int((M_Img_w - S_Img_w) / 2)
    w1 = int((M_Img_w - S_Img_w1) / 2)
    h = int((M_Img_h - S_Img_h) / 2)
    h1 = int((M_Img_h - S_Img_h1) / 2)

    try:
        if coordinate == None or coordinate == "":
            coordinate = (w, h)
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
            coordinate = (w1, h1)
            M_Img.paste(icon1, coordinate, mask=None)
        else:
            print("已经指定坐标")
            # 粘贴子图到母图的指定坐标
            M_Img.paste(icon, coordinate, mask=None)
            coordinate = (10, 10)
            M_Img.paste(icon1, coordinate, mask=None)
    except:
        print("坐标指定出错 ")
    # 保存图片
    M_Img.save(save_img)


def draw_image(template_img, user_sex, title, maths, user_id):  # 获取答题结果内容，生成报告
    math_type_info = AnswerInfo.objects.get(user_id=user_id)
    math_count_dict = ast.literal_eval(math_type_info.titleCount)
    # 图片名称
    img = template_img  # 图片模板
    new_img = './static/image/app/text_%s.png' % user_id  # 生成的图片

    # 设置字体样式
    font_type = './static/font/msyhl.ttc'
    font_medium_type = './static/font/msyhl.ttc'

    title_font = ImageFont.truetype(font_medium_type, 20)
    font = ImageFont.truetype(font_type, 18)
    cur_time_font = ImageFont.truetype(font_type, 16)
    color = "#000000"
    color1 = "blue"
    color2 = "red"

    # 打开图片
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # 标题
    title_x = 90
    title_y = height - 180

    if int(user_sex) == 0:
        sex = '♀'
    elif int(user_sex) == 1:
        sex = '♂'
    else:
        sex = '⚥'
    draw.text((title_x + 10, height - title_y + 10), u'%s%s 小朋友' % (title, sex), color, title_font)
    # draw.text((title_x + 40, height - title_y + 10), u'%s' % title, color1, title_font)

    # 答题完成时间
    # cur_time = '在' + '%s年%s月%s日 ' % (
    #     time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday,) + time.strftime("%H:%M:%S",
    #                                                                                                   time.localtime())
    cur_time = '在 %s ，完成了 %s 道 %s 题' % (
        math_type_info.updateTime.strftime("%Y-%m-%d %H:%M:%S"),
        math_count_dict['mathCount']['Count'],
        math_type_info.get_titleGrade_display())
    # cur_time = '在 %s ，完成了 %s 道' % (
    #     math_type_info.updateTime.strftime("%Y-%m-%d %H:%M:%S"),
    #     math_type_info.titleCount,
    #     math_type_info.get_mathGrade_display())
    cur_time_x = title_x + 10
    cur_time_y = title_y - 50
    draw.text((cur_time_x, height - cur_time_y), u'%s' % cur_time, color1, cur_time_font)

    # 题数
    cur_time_x = title_x + 10
    cur_time_y = title_y - 75
    total_time = math_type_info.endTime - math_type_info.startTime
    if total_time <= 60:  # 计算秒
        use_time = '共提交 %s 次，用时 %s秒' % (math_type_info.submitNumber, total_time)
    elif 60 < total_time <= 60 * 60:  # 计算分
        m = math.modf(total_time / 60)
        use_time = '共提交 %s 次，用时 %s分%s秒' % (math_type_info.submitNumber, math.ceil(m[1]), math.ceil(m[0] * 60))
    elif 60 * 60 < total_time <= 60 * 60 * 24:  # 计算时
        h = math.modf(total_time / 3600)
        m = math.modf(h[0] * 60)
        use_time = '共提交 %s 次，用时 %s小时%s分%s秒' % (
            math_type_info.submitNumber, math.ceil(h[1]), math.ceil(m[1]), math.ceil(m[0] * 60))
    else:  # 计算天
        t = math.modf(total_time / (3600 * 24))
        h = math.modf(t[0] * 24)
        m = math.modf(h[0] * 60)
        use_time = '共提交 %s 次，用时 %s天%s小时%s分%s秒' % (
            math_type_info.submitNumber, math.ceil(t[1]), math.ceil(h[1]), math.ceil(m[1]), math.ceil(m[0] * 60))
    draw.text((cur_time_x, height - cur_time_y), u'%s' % use_time, color1, cur_time_font)

    # 运算题目
    math_x = title_x + 10
    math_start_y = title_y - 180
    math_line = 30
    if len(maths) < 10:
        for num, titleName in enumerate(maths):
            y = math_start_y - num * math_line
            draw.text((math_x, height - y), u'%s' % titleName, color, font)
    else:
        for num, mathDict in enumerate(maths):
            y = math_start_y - num * math_line
            if num < len(maths) / 2:
                if mathDict['answerComparison'] is True:
                    draw.text((math_x - 60, height - y), u'%s.  %s' % (num + 1, mathDict['titleName']), color, font)
                else:
                    draw.text((math_x - 60, height - y), u'%s.  %s' % (num + 1, mathDict['titleName']), color2, font)
            else:
                if len(maths) % 2 == 0:
                    if mathDict['answerComparison'] is True:
                        draw.text((width / 2 + 10, height - y - len(maths) / 2 * 30),
                                  u'%s.  %s' % (num + 1, mathDict['titleName']), color, font)
                    else:
                        draw.text((width / 2 + 10, height - y - len(maths) / 2 * 30),
                                  u'%s.  %s' % (num + 1, mathDict['titleName']), color2, font)
                else:
                    if mathDict['answerComparison'] is True:
                        draw.text((width / 2 + 10, height - y - (len(maths) + 1) / 2 * 30),
                                  u'%s.  %s' % (num + 1, mathDict['titleName']), color, font)
                    else:
                        draw.text((width / 2 + 10, height - y - (len(maths) + 1) / 2 * 30),
                                  u'%s.  %s' % (num + 1, mathDict['titleName']), color2, font)

    # 生成图片
    image.save(new_img, 'png')


# 幼儿园答题结果页
@login_required
def result(request):
    user_id = request.session.get('_auth_user_id')
    maths_obj = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=0).order_by('titleGrade').all()
    user_sex = request.session.get('sex')
    class_list = maths_obj.values('titleGrade')
    print('计算题类型：', class_list)

    maths_list = []
    for item in maths_obj:
        maths_list.append({'titleName': item.titleName,
                           'rightAnswer': item.rightAnswer,
                           'inputAnswer': item.inputAnswer,
                           'answerComparison': item.answerComparison})
    print(maths_list)

    result_true = []
    maths = []
    maths_comparison = []
    for i, item in enumerate(maths_list):
        maths_comparison.append(item['answerComparison'])
        if int(class_list[i]['titleGrade']) == 3:
            # 把字符串转为 list
            str_list = list(item['titleName'])
            # 找到反括号的位置
            nPos = str_list.index(')')
            str_list.insert(nPos, "%s " % item['inputAnswer'])  # 在反括号位置之前 插入要插入的字符
            # 将 list 转为 str，并传入maths = []
            maths.append({'titleName': "".join(str_list), 'answerComparison': item['answerComparison']})
            if item['answerComparison'] is False:  # 判断答题是否正确，如果错误，将正确的答案返回到result_true列表中
                str_list = list(item['titleName'])
                nPos = str_list.index(')')
                str_list.insert(nPos, "%s " % item['rightAnswer'])
                result_true.append({'num': i + 1, 'result': "".join(str_list)})
        else:
            maths.append(
                {'titleName': item['titleName'] + item['inputAnswer'], 'answerComparison': item['answerComparison']})
            if item['answerComparison'] is False:
                result_true.append({'num': i + 1, 'result': item['titleName'] + item['rightAnswer']})

    print(maths)
    width = 496
    height = 681
    for i in range(len(maths_obj)):
        if len(maths_obj) < 10:
            height += 28
        else:
            height += 14
            new_image(width, height, color='#EFD07D')

    synthesis_image(mother_img='./static/image/app/test.png',
                    son_img='./static/image/app/son_img1.png',
                    son_img1='./static/image/app/son_img2.png',
                    save_img='./static/image/app/save_img_user_%s.png' % user_id, coordinate=(0, height - 270))

    title = '%s ' % request.session.get('user')
    template_img = './static/image/app/save_img_user_%s.png' % user_id

    draw_image(template_img, user_sex, title, maths, user_id)

    return render(request, 'result.html', {'yes': Counter(maths_comparison)[True],
                                           'no': Counter(maths_comparison)[False],
                                           'user_id': user_id,
                                           'result_true': result_true,
                                           'FalseNum': len(result_true),
                                           'submitNum': AnswerInfo.objects.get(user_id=user_id).submitNumber,
                                           })


# 1-6年级答题结果页
@login_required
def result_class(request):
    pass
    return render(request, 'result_class.html')


# 默认首页
@login_required
def home(request):
    user_id = request.session.get('_auth_user_id')  # 获取用户id
    user_profile = UserProfile.objects.get(user_id=user_id)

    if request.POST:
        math_type = request.POST.get('mathType', None)  # 获取题目类型
        math_count_amount = request.POST.get('mathCount', None)  # 获取题目数量
        math_number_range = request.POST.get('numberRange', None)  # 获取题目范围
        math_grade = request.POST.get('mathGrade', None)  # 获取题目难易程度
        # fill_amount = request.POST.get('mathFill', None)  # 获取填空题题数
        # select_amount = request.POST.get('mathSelect', None)  # 获取选择题题数
        # verdict_amount = request.POST.get('mathVerdict', None)  # 获取判断题题数
        # use_amount = request.POST.get('mathUse', None)  # 获取应用题题数
        # number_amount = request.POST.get('mathNumber', None)  # 获取奥数题题数
        user_select_class = request.POST.get('selectClass', None)  # 获取用户选则的年级

        print('用户id:', user_id)
        print('题目类型', math_type)
        print('题目范围', math_number_range)
        print('计算题数量', math_count_amount)
        print('题目难易', math_grade)
        # print('填空题数量', fill_amount)
        # print('选择题数量', select_amount)
        # print('判断题数量', verdict_amount)
        # print('应用题数量', use_amount)
        # print('奥数题数量', number_amount)
        print('用户选中的年级', user_select_class)

        if int(user_select_class) == 0:
            SelectTitleInfo.objects.filter(user_id=user_id).delete()  # 删除数据库中SelectTitleInfo的数据
            AnswerInfo.objects.filter(user_id=user_id).delete()  # 删除数据库中AnswerInfo的数据
            models.AnswerInfo.objects.create(user_id=user_id,
                                             userSelectClass=user_select_class,
                                             titleCount={'mathCount': {'Type': '0', 'titleType': math_type,
                                                                       'Count': math_count_amount,
                                                                       'Range': math_number_range},
                                                         'mathFill': {'Type': '1', 'Fill': 0},
                                                         'mathSelect': {'Type': '2', 'Select': 0},
                                                         'mathVerdict': {'Type': '3', 'Verdict': 0},
                                                         'mathUse': {'Type': '4', 'Use': 0},
                                                         'mathNumber': {'Type': '5', 'Number': 0}},
                                             titleGrade=math_grade,
                                             startTime=time.time())
            for i in range(int(math_count_amount)):
                if int(math_number_range) < 20:
                    x = random.randint(0, int(math_number_range))
                    y = random.randint(0, int(math_number_range))
                    z = random.randint(0, int(math_number_range))
                elif int(math_number_range) > 50:
                    x = random.randint(10, int(math_number_range))
                    y = random.randint(10, int(math_number_range))
                    z = random.randint(10, int(math_number_range))
                else:
                    x = random.randint(5, int(math_number_range))
                    y = random.randint(5, int(math_number_range))
                    z = random.randint(5, int(math_number_range))
                if int(math_type) == 1:  # 加减法
                    if int(math_grade) == 1:  # 简单
                        math1(x, y, i, user_id)
                    elif int(math_grade) == 2:  # 适中
                        if i < int(math_count_amount) / 4:
                            math1(x, y, i, user_id)
                        elif (int(math_count_amount) / 4) < i < (int(math_count_amount) / 2):
                            math3(x, y, z, i, user_id)
                        else:
                            math2(x, y, z, i, user_id)

                    elif int(math_grade) == 3:  # 偏难
                        if i < int(math_count_amount) / 4:
                            math2(x, y, z, i, user_id)
                        elif (int(math_count_amount) / 4) < i < (int(math_count_amount) / 2):
                            math3(x, y, z, i, user_id)
                        else:
                            math1(x, y, i, user_id)

                    else:  # 特难
                        if i < int(math_count_amount) / 2:
                            math2(x, y, z, i, user_id)
                        else:
                            math3(x, y, z, i, user_id)
                elif int(math_type) == 2:  # 乘除法
                    if int(math_grade) == 1:
                        math4(x, y, i, user_id)
                    elif int(math_grade) == 2:
                        if i < int(math_count_amount) / 2:
                            math4(x, y, i, user_id)
                        else:
                            math5(x, y, z, i, user_id)
                    elif int(math_grade) == 3:
                        if i > int(math_count_amount) / 2:
                            math4(x, y, i, user_id)
                        elif i > (int(math_count_amount) / 2) / 2:
                            math5(x, y, z, i, user_id)
                        else:
                            math6(x, y, z, i, user_id)
                    else:
                        if i > int(math_count_amount) / 2:
                            math5(x, y, z, i, user_id)
                        else:
                            math6(x, y, z, i, user_id)
                else:  # 加减乘除法
                    if int(math_grade) == 1:
                        math7(x, y, z, i, user_id)
                    elif int(math_grade) == 2:
                        math7(x, y, z, i, user_id)
                    elif int(math_grade) == 3:
                        math7(x, y, z, i, user_id)
                    else:
                        math7(x, y, z, i, user_id)

            response = HttpResponseRedirect('/index/')
            return response
        else:
            SelectTitleInfo.objects.filter(user_id=user_id).delete()  # 删除数据库中SelectTitleInfo的数据
            AnswerInfo.objects.filter(user_id=user_id).delete()  # 删除数据库中AnswerInfo的数据
            models.AnswerInfo.objects.create(user_id=user_id,
                                             userSelectClass=user_select_class,
                                             titleCount={'mathCount': {'Type': '0', 'titleType': math_type,
                                                                       'Count': math_count_amount,
                                                                       'Range': math_number_range},
                                                         'mathFill': {'Type': '1', 'Fill': 10},
                                                         'mathSelect': {'Type': '2', 'Select': 10},
                                                         'mathVerdict': {'Type': '3', 'Verdict': 10},
                                                         'mathUse': {'Type': '4', 'Use': 5},
                                                         'mathNumber': {'Type': '5', 'Number': 2}},
                                             titleGrade=math_grade,
                                             startTime=time.time())
            """随机生成的计算题"""
            # 计算题
            for i in range(int(math_count_amount)):
                if int(math_number_range) < 20:
                    x = random.randint(0, int(math_number_range))
                    y = random.randint(0, int(math_number_range))
                    z = random.randint(0, int(math_number_range))
                elif int(math_number_range) > 50:
                    x = random.randint(10, int(math_number_range))
                    y = random.randint(10, int(math_number_range))
                    z = random.randint(10, int(math_number_range))
                else:
                    x = random.randint(5, int(math_number_range))
                    y = random.randint(5, int(math_number_range))
                    z = random.randint(5, int(math_number_range))
                if int(math_type) == 1:  # 加减法
                    if int(math_grade) == 1:  # 简单
                        math1(x, y, i, user_id)
                    elif int(math_grade) == 2:  # 适中
                        if i < int(math_count_amount) / 2:
                            math1(x, y, i, user_id)
                        else:
                            math2(x, y, z, i, user_id)
                    elif int(math_grade) == 3:  # 偏难
                        if i < int(math_count_amount) / 4:
                            math2(x, y, z, i, user_id)
                        elif (int(math_count_amount) / 4) < i < (int(math_count_amount) / 2):
                            math3(x, y, z, i, user_id)
                        else:
                            math1(x, y, i, user_id)

                    else:  # 特难
                        if i < int(math_count_amount) / 2:
                            math2(x, y, z, i, user_id)
                        else:
                            math3(x, y, z, i, user_id)
                elif int(math_type) == 2:  # 乘除法
                    if int(math_grade) == 1:
                        math4(x, y, i, user_id)
                    elif int(math_grade) == 2:
                        if i < int(math_count_amount) / 2:
                            math4(x, y, i, user_id)
                        else:
                            math5(x, y, z, i, user_id)
                    elif int(math_grade) == 3:
                        if i > int(math_count_amount) / 2:
                            math4(x, y, i, user_id)
                        elif i > (int(math_count_amount) / 2) / 2:
                            math5(x, y, z, i, user_id)
                        else:
                            math6(x, y, z, i, user_id)
                    else:
                        if i > int(math_count_amount) / 2:
                            math5(x, y, z, i, user_id)
                        else:
                            math6(x, y, z, i, user_id)
                else:  # 加减乘除法
                    if int(math_grade) == 1:
                        math7(x, y, z, i, user_id)
                    elif int(math_grade) == 2:
                        math7(x, y, z, i, user_id)
                    elif int(math_grade) == 3:
                        math7(x, y, z, i, user_id)
                    else:
                        math7(x, y, z, i, user_id)

            """随机从数据库中获取对应题数的数据，并保存到答题题库"""
            math_title(10, 10, 10, 5, 2, user_select_class, user_id)

            response = HttpResponseRedirect('/index/')
            return response

    try:
        math_type_info = AnswerInfo.objects.get(user_id=user_id)
        new_result_dict = SelectTitleInfo.objects.filter(user_id=user_id).values('inputAnswer').all()
        new_result_list = []
        for item in new_result_dict:
            new_result_list.append(item['inputAnswer'])
        differences = None in Counter(new_result_list).keys()  # differences判断填写的结果是否存在空值
        if differences is False:
            return render(request, 'home.html',
                          {'result': math_type_info.endTime,
                           'userId': math_type_info.user_id,
                           'userClass': int(user_profile.userClass),
                           'user_select_class': int(math_type_info.userSelectClass),
                           'persona': int(user_profile.userPersona),
                           'user_class': user_profile.get_userClass_display()})
        else:
            return render(request, 'home.html',
                          {'result': None,
                           'userId': math_type_info.user_id,
                           'userClass': int(user_profile.userClass),
                           'user_select_class': int(math_type_info.userSelectClass),
                           'persona': int(user_profile.userPersona),
                           'user_class': user_profile.get_userClass_display()})
    except:
        return render(request, 'home.html',
                      {'result': None,
                       'userId': None,
                       'userClass': int(user_profile.userClass),
                       'user_select_class': None,
                       'persona': int(user_profile.userPersona),
                       'user_class': user_profile.get_userClass_display()})


# 自定义首页
@login_required
def custom_home(request):
    user_id = request.session.get('_auth_user_id')  # 获取用户id
    user_profile = UserProfile.objects.get(user_id=user_id)
    if request.POST:
        math_type = request.POST.get('mathType', None)  # 获取题目类型
        user_select_class = request.POST.get('selectClass', None)  # 获取用户选则的年级
        math_count_amount = request.POST.get('mathCount', None)  # 获取题目数量
        math_number_range = request.POST.get('numberRange', None)  # 获取题目范围
        math_grade = request.POST.get('mathGrade', None)  # 获取题目难易程度
        fill_amount = request.POST.get('mathFill', None)  # 获取填空题题数
        select_amount = request.POST.get('mathSelect', None)  # 获取选择题题数
        verdict_amount = request.POST.get('mathVerdict', None)  # 获取判断题题数
        use_amount = request.POST.get('mathUse', None)  # 获取应用题题数
        number_amount = request.POST.get('mathNumber', None)  # 获取奥数题题数

        print('用户id:', user_id)
        print('用户选中的年级：', user_select_class)
        print('口算题目类型：', math_type)
        print('口算题目范围：', math_number_range)
        print('口算题目难易：', math_grade)
        print('口算题数量：', math_count_amount)
        print('填空题数量：', fill_amount)
        print('选择题数量：', select_amount)
        print('判断题数量：', verdict_amount)
        print('应用题数量：', use_amount)
        print('奥数题数量：', number_amount)

        SelectTitleInfo.objects.filter(user_id=user_id).delete()  # 删除数据库中SelectTitleInfo的数据
        AnswerInfo.objects.filter(user_id=user_id).delete()  # 删除数据库中AnswerInfo的数据

        """更新AnswerInfo中的数据"""
        models.AnswerInfo.objects.create(user_id=user_id,
                                         userSelectClass=user_select_class,
                                         titleCount={'mathCount': {'Type': '0', 'titleType': math_type,
                                                                   'Count': math_count_amount,
                                                                   'Range': math_number_range},
                                                     'mathFill': {'Type': '1', 'Fill': fill_amount},
                                                     'mathSelect': {'Type': '2', 'Select': select_amount},
                                                     'mathVerdict': {'Type': '3', 'Verdict': verdict_amount},
                                                     'mathUse': {'Type': '4', 'Use': use_amount},
                                                     'mathNumber': {'Type': '5', 'Number': number_amount}},
                                         titleGrade=math_grade,
                                         startTime=time.time())
        """随机生成的计算题"""
        # 计算题
        for i in range(int(math_count_amount)):
            x = random.randint(0, int(math_number_range))
            y = random.randint(0, int(math_number_range))
            z = random.randint(0, int(math_number_range))
            if int(math_type) == 1:  # 加减法
                if int(math_grade) == 1:  # 简单
                    math1(x, y, i, user_id)
                elif int(math_grade) == 2:  # 适中
                    if i < int(math_count_amount) / 2:
                        math1(x, y, i, user_id)
                    else:
                        math2(x, y, z, i, user_id)
                elif int(math_grade) == 3:  # 偏难
                    if i < int(math_count_amount) / 4:
                        math2(x, y, z, i, user_id)
                    elif (int(math_count_amount) / 4) < i < (int(math_count_amount) / 2):
                        math3(x, y, z, i, user_id)
                    else:
                        math1(x, y, i, user_id)

                else:  # 特难
                    if i < int(math_count_amount) / 2:
                        math2(x, y, z, i, user_id)
                    else:
                        math3(x, y, z, i, user_id)
            elif int(math_type) == 2:  # 乘除法
                if int(math_grade) == 1:
                    math4(x, y, i, user_id)
                elif int(math_grade) == 2:
                    if i < int(math_count_amount) / 2:
                        math4(x, y, i, user_id)
                    else:
                        math5(x, y, z, i, user_id)
                elif int(math_grade) == 3:
                    if i > int(math_count_amount) / 2:
                        math4(x, y, i, user_id)
                    elif i > (int(math_count_amount) / 2) / 2:
                        math5(x, y, z, i, user_id)
                    else:
                        math6(x, y, z, i, user_id)
                else:
                    if i > int(math_count_amount) / 2:
                        math5(x, y, z, i, user_id)
                    else:
                        math6(x, y, z, i, user_id)
            else:  # 加减乘除法
                if int(math_grade) == 1:
                    math7(x, y, z, i, user_id)
                elif int(math_grade) == 2:
                    math7(x, y, z, i, user_id)
                elif int(math_grade) == 3:
                    math7(x, y, z, i, user_id)
                else:
                    math7(x, y, z, i, user_id)

        """随机从数据库中获取对应题数的数据，并保存到答题题库"""
        math_title(fill_amount, select_amount, verdict_amount, use_amount, number_amount, user_select_class, user_id)

        response = HttpResponseRedirect('/index/')
        return response
    try:
        math_type_info = AnswerInfo.objects.get(user_id=user_id)
        new_result_dict = SelectTitleInfo.objects.filter(user_id=user_id).values('inputAnswer').all()
        new_result_list = []
        for item in new_result_dict:
            new_result_list.append(item['inputAnswer'])
        differences = None in Counter(new_result_list).keys()

        if differences is False:
            return render(request, 'custom_home.html',
                          {'result': math_type_info.endTime,
                           'userId': math_type_info.user_id,
                           'userClass': int(user_profile.userClass),
                           'user_class': user_profile.get_userClass_display()})
        else:
            return render(request, 'custom_home.html',
                          {'result': None,
                           'userId': math_type_info.user_id,
                           'userClass': int(user_profile.userClass),
                           'user_class': user_profile.get_userClass_display()})
    except:
        return render(request, 'custom_home.html',
                      {'result': None,
                       'userId': None,
                       'userClass': int(user_profile.userClass),
                       'user_class': user_profile.get_userClass_display()})


# 幼儿园算式页
# @login_required
# def index_0(request):
#     user_id = request.session.get('_auth_user_id')
#     num_list = Math.objects.filter(user_id=user_id).order_by('mathClass').all()
#     nid = Math.objects.filter(user_id=user_id).values('id').all()
#     rightAnswerDict = Math.objects.filter(user_id=user_id).values('rightAnswer').all()
#     answerComparisonDict = Math.objects.filter(user_id=user_id).values('answerComparison').all()
#     math = Mathinfo.objects.get(user_id=user_id)
#
#     if request.POST:
#         textList = []
#         resultList = []
#         inputAnswerDict = Math.objects.filter(user_id=user_id).values('inputAnswer').all()
#         submitNumber = models.Mathinfo.objects.filter(user_id=user_id).values('submitNumber').all()
#         submitNumber1 = models.Mathinfo.objects.filter(user_id=user_id).values('titleType').all()
#
#         print('题目类型》》》》', math.get_titleType_display())  # 获取modes中choices字段
#         print('====================', submitNumber1)
#         for i in range(len(rightAnswerDict)):
#             '''判断所有结果是否有改动,无改动，取上一次的值'''
#             answer_input = request.POST.get('text%s' % nid[i]['id'], None)
#             if answer_input is None:
#                 models.Math.objects.filter(id=nid[i]['id']).update(
#                     inputAnswer=inputAnswerDict[i]['inputAnswer'])  # 更新数据库
#                 textList.append(inputAnswerDict[i]['inputAnswer'])  # 更新内存list
#             else:
#                 textList.append(answer_input)
#                 models.Math.objects.filter(id=nid[i]['id']).update(inputAnswer='%s' % answer_input)
#             resultList.append(rightAnswerDict[i]['rightAnswer'])
#
#         if textList == resultList:
#             models.Mathinfo.objects.filter(user_id=user_id).update(submitNumber=submitNumber[0]['submitNumber'] + 1,
#                                                                    updateTime=datetime.datetime.now(),
#                                                                    endTime=time.time())
#             for i in range(len(rightAnswerDict)):
#                 models.Math.objects.filter(id=nid[i]['id']).update(answerComparison=True)
#             response = HttpResponseRedirect('/result/')
#             return response
#         else:
#             models.Mathinfo.objects.filter(user_id=user_id).update(submitNumber=submitNumber[0]['submitNumber'] + 1,
#                                                                    updateTime=datetime.datetime.now(),
#                                                                    endTime=time.time())
#             for i in range(len(rightAnswerDict)):
#                 if textList[i] == resultList[i]:
#                     models.Math.objects.filter(id=nid[i]['id']).update(answerComparison=True)
#                 else:
#                     models.Math.objects.filter(id=nid[i]['id']).update(answerComparison=False)
#
#         response = HttpResponseRedirect('/result/')
#         return response
#         # cdict = []
#         # for k in range(len(answerComparisonDict)):
#         #     cdict.append(answerComparisonDict[k]['answerComparison'])
#         # print('提交答案之后，判断对错各有多少个：', Counter(cdict))
#         # differences = Counter(cdict)
#         # return render(request, 'index_0.html',
#         #               {'num': num_list,
#         #                'yes': differences[True],
#         #                'no': differences[False],
#         #                'type': math.get_titleType_display(),
#         #                'grade': math.get_mathGrade_display(),
#         #                'count': math.titleCount,
#         #                'submitNum': math.submitNumber + 1})
#
#     ComparisonDict = []
#     for k in range(len(answerComparisonDict)):
#         ComparisonDict.append(answerComparisonDict[k]['answerComparison'])
#     print('判断是否为空：', Counter(ComparisonDict))
#     differences = Counter(ComparisonDict)
#     print('' in differences.keys())  # 使用in方法,查看某一个key是否在字典中存在，也可使用print('' in differences)
#     return render(request, 'index_0.html', {
#         'num': num_list,
#         'yes': differences[True],
#         'no': differences[False],
#         'num_null': None in differences.keys(),
#         'type': math.get_titleType_display(),
#         'grade': math.get_mathGrade_display(),
#         'count': math.titleCount,
#         'submitNum': math.submitNumber})


@login_required  # 小学0-6年级算式页
def index(request):
    user_id = request.session.get('_auth_user_id')
    math_list = SelectTitleInfo.objects.filter(user_id=user_id).all()
    math_type_info_list = AnswerInfo.objects.get(user_id=user_id)
    math_count_dict = ast.literal_eval(math_type_info_list.titleCount)
    math_comparison_dict = math_list.values('answerComparison')
    # user_profile = UserProfile.objects.get(user_id=user_id)
    # nid = Math.objects.filter(user_id=user_id).values('id').all()
    # math_result_dict = SelectTitleInfo.objects.filter(user_id=user_id).values('rightAnswer').all()
    # math_comparison_dict = Math.objects.filter(user_id=user_id).values('answerComparison').all()
    # print(math_count_dict['fill']['mathFill'])
    # print(len(math_title_list))
    # print(math_list.values('rightAnswer'))
    # print(math_list.values('id'))
    # print(math_list.values('answerComparison'))

    count_list = []  # 计算题
    if int(math_count_dict['mathCount']['Count']) != 0:
        math_count_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=0).order_by(
            'titleGrade').all()
        for item in math_count_list:
            count_list.append(item)
    else:
        count_list = None
    print(count_list)

    fill_list = []  # 填空题
    if int(math_count_dict['mathFill']['Fill']) != 0:
        math_fill_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=1).all()
        for item in math_fill_list:
            fill_list.append(item)
    else:
        fill_list = None
    print(fill_list)

    select_list = []  # 选择题
    if int(math_count_dict['mathSelect']['Select']) != 0:
        math_select_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=2).all()
        for item in math_select_list:
            select_list.append(item)
    else:
        select_list = None
    print(select_list)

    verdict_list = []  # 判断题
    if int(math_count_dict['mathVerdict']['Verdict']) != 0:
        math_verdict_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=3).all()
        for item in math_verdict_list:
            verdict_list.append(item)
    else:
        verdict_list = None
    print(verdict_list)

    use_list = []  # 应用题
    if int(math_count_dict['mathUse']['Use']) != 0:
        math_use_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=4).all()
        for item in math_use_list:
            use_list.append(item)
    else:
        use_list = None
    print(use_list)

    number_list = []  # 奥数题
    if int(math_count_dict['mathNumber']['Number']) != 0:
        math_number_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=5).all()
        for item in math_number_list:
            number_list.append(item)
    else:
        number_list = None
    print(number_list)

    if request.POST:
        math_id = math_list.values('id')
        math_result = math_list.values('rightAnswer')
        math_new_result = math_list.values('inputAnswer')

        for i in range(len(math_list)):
            """向数据库更新提交次数"""
            models.AnswerInfo.objects.filter(user_id=user_id).update(
                submitNumber=int(math_type_info_list.submitNumber) + 1,
                updateTime=datetime.datetime.now(),
                endTime=time.time())
            '''判断所有结果是否有改动,无改动，取上一次的值'''
            answer_get = request.POST.getlist('%s' % math_id[i]['id'], None)  # 获取用户输入的内容
            print('%s' % math_id[i]['id'], answer_get)
            if answer_get is None:
                models.SelectTitleInfo.objects.filter(id=math_id[i]['id']).update(
                    inputAnswer=math_new_result[i]['inputAnswer'],
                    answerComparison=False)  # 更新数据库
            elif answer_get == '':
                models.SelectTitleInfo.objects.filter(id=math_id[i]['id']).update(
                    inputAnswer=math_new_result[i]['inputAnswer'],
                    answerComparison=False)  # 更新数据库
            else:
                result_get = math_result[i]['rightAnswer']
                if answer_get == result_get.split(','):
                    models.SelectTitleInfo.objects.filter(id=math_id[i]['id']).update(
                        inputAnswer='%s' % ','.join(answer_get),
                        answerComparison=True)  # 更新数据库
                else:
                    models.SelectTitleInfo.objects.filter(id=math_id[i]['id']).update(
                        inputAnswer='%s' % ','.join(answer_get),
                        answerComparison=False)  # 更新数据库
        if int(math_type_info_list.userSelectClass) == 0:
            response = HttpResponseRedirect('/result/')
            return response
        else:
            response = HttpResponseRedirect('/result_class/')
            return response

    comparison_dict = []
    for i in range(len(math_comparison_dict)):
        comparison_dict.append(math_comparison_dict[i]['answerComparison'])
    # print('判断是否为空：', Counter(comparison_dict))
    differences = Counter(comparison_dict)
    # print('' in differences.keys())  # 使用in方法,查看某一个key是否在字典中存在，也可使用print('' in differences)

    math_fill_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=1).all()
    fill_id_list = math_fill_list.values('id')
    fill_title_list = math_fill_list.values('titleName')
    fill_new_result_list = math_fill_list.values('inputAnswer')
    fill_comparison_list = math_fill_list.values('answerComparison')
    math_fill_dict = []
    for i in range(len(math_fill_list)):
        if fill_new_result_list[i]['inputAnswer'] is None:
            math_fill_dict.append({'id': fill_id_list[i]['id'],
                                   'titleName': fill_title_list[i]['titleName'],
                                   'inputAnswer': '',
                                   'answerComparison': fill_comparison_list[i]['answerComparison']})
        else:
            math_fill_dict.append({'id': fill_id_list[i]['id'],
                                   'titleName': fill_title_list[i]['titleName'],
                                   'inputAnswer': fill_new_result_list[i]['inputAnswer'],
                                   'answerComparison': fill_comparison_list[i]['answerComparison']})
    print(math_fill_dict)

    math_select_list = SelectTitleInfo.objects.filter(user_id=user_id).filter(titleType=2).all()
    select_id_list = math_select_list.values('id')
    select_title_list = math_select_list.values('titleName')
    select_subjoin_title_list = math_select_list.values('titleSubjoin')
    select_new_result_list = math_select_list.values('inputAnswer')
    select_comparison_list = math_select_list.values('answerComparison')
    math_select_dict = []
    for i in range(len(math_select_list)):
        if select_new_result_list[i]['inputAnswer'] is None:
            math_select_dict.append({'id': select_id_list[i]['id'],
                                     'titleName': select_title_list[i]['titleName'],
                                     'titleSubjoin': select_subjoin_title_list[i]['titleSubjoin'],
                                     'inputAnswer': '',
                                     'answerComparison': select_comparison_list[i]['answerComparison']})
        else:
            math_select_dict.append({'id': select_id_list[i]['id'],
                                     'titleName': select_title_list[i]['titleName'],
                                     'titleSubjoin': select_subjoin_title_list[i]['titleSubjoin'],
                                     'inputAnswer': select_new_result_list[i]['inputAnswer'],
                                     'answerComparison': select_comparison_list[i]['answerComparison']})
    print(math_select_dict)

    return render(request, 'index.html', {
        'comparison_true': differences[True],
        'comparison_false': differences[False],
        'comparison_none': None in differences.keys(),
        'fill': fill_list,  # 填空题
        'f_fill': json.dumps(math_fill_dict),  # 填空题
        'count': count_list,  # 计算题
        'select': select_list,  # 选择题
        's_select': json.dumps(math_select_dict),  # 选择题
        'verdict': verdict_list,  # 判断题
        'use': use_list,  # 应用题
        'number': number_list})  # 奥数题


def title_add(request):
    pass
    # form = TitleAddForm()
    # return render(request, 'title_add.html', {'form': form})
    return render(request, 'title_add.html')


# ---根据用户自定义的题数以及年级，随机从数据库中获取对应的题目数据，并保存到答题题库---
def math_title(fill_amount, select_amount, verdict_amount, use_amount, number_amount, user_select_class, user_id):
    # 填空题
    if int(fill_amount) != 0:
        # num_list = Math.objects.order_by('?')[:2]  # 随机从数据库取出指定条数的数据,弊端：每个字段数据不对应，只取一个字段数据可用
        num = TitleStore.objects.filter(applyClass=user_select_class).filter(titleType=1)
        math_id = []
        for item in num:
            math_id.append(item.id)  # 将该题型的所有id获取到list中，以便取随机值
        for num, item in enumerate(random.sample(math_id, int(fill_amount))):  # 使用random.sample取指定的随机值，并遍历循环
            title = TitleStore.objects.get(id=item)
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleType=title.titleType,
                                                  Course=title.Course,
                                                  titleName=str(num + 1) + '. ' + title.titleName,
                                                  titleImage=title.titleImage,
                                                  rightAnswer=title.titleAnswer,
                                                  titleAnalysis=title.titleAnalysis)
    # 选择题
    if int(select_amount) != 0:
        num = TitleStore.objects.filter(applyClass=user_select_class).filter(titleType=2)
        # print('============', ast.literal_eval(num[0].titleName)['title'])  # 用ast.literal_eval将字符串转变为字典
        math_id = []
        for item in num:
            math_id.append(item.id)
        for num, item in enumerate(random.sample(math_id, int(select_amount))):
            title = TitleStore.objects.get(id=item)
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleType=title.titleType,
                                                  Course=title.Course,
                                                  titleName=str(num + 1) + '、' + title.titleName,
                                                  titleSubjoin=title.titleSubjoin,
                                                  titleImage=title.titleImage,
                                                  rightAnswer=title.titleAnswer,
                                                  titleAnalysis=title.titleAnalysis)
    # # 判断题
    if int(verdict_amount) != 0:
        num = TitleStore.objects.filter(applyClass=user_select_class).filter(titleType=3)
        math_id = []
        for item in num:
            math_id.append(item.id)
        for num, item in enumerate(random.sample(math_id, int(verdict_amount))):
            title = TitleStore.objects.get(id=item)
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleType=title.titleType,
                                                  Course=title.Course,
                                                  titleName=str(num + 1) + '、' + title.titleName,
                                                  titleSubjoin=title.titleSubjoin,
                                                  titleImage=title.titleImage,
                                                  rightAnswer=title.titleAnswer,
                                                  titleAnalysis=title.titleAnalysis)
    # 应用题
    if int(use_amount) != 0:
        num = TitleStore.objects.filter(applyClass=user_select_class).filter(titleType=4)
        math_id = []
        for item in num:
            math_id.append(item.id)
        for num, item in enumerate(random.sample(math_id, int(use_amount))):
            title = TitleStore.objects.get(id=item)
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleType=title.titleType,
                                                  Course=title.Course,
                                                  titleName=str(num + 1) + '、' + title.titleName,
                                                  titleSubjoin=title.titleSubjoin,
                                                  titleImage=title.titleImage,
                                                  rightAnswer=title.titleAnswer,
                                                  titleAnalysis=title.titleAnalysis)
    # # 奥数题
    if int(number_amount) != 0:
        num = TitleStore.objects.filter(applyClass=user_select_class).filter(titleType=5)
        math_id = []
        for item in num:
            math_id.append(item.id)
        for num, item in enumerate(random.sample(math_id, int(number_amount))):
            title = TitleStore.objects.get(id=item)
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleType=title.titleType,
                                                  Course=title.Course,
                                                  titleName=str(num + 1) + '、' + title.titleName,
                                                  titleSubjoin=title.titleSubjoin,
                                                  titleImage=title.titleImage,
                                                  rightAnswer=title.titleAnswer,
                                                  titleAnalysis=title.titleAnalysis)


def math1(x, y, i, user_id):  # 简单加减
    if i % 2 == 0:
        if x > y:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s - %s = ' % (x, y),
                                                  rightAnswer=x - y)
        else:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s + %s = ' % (x, y),
                                                  rightAnswer=x + y)
    else:
        if x > y:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s - %s = ' % (x, y),
                                                  rightAnswer=x - y)
        else:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s + %s  = ' % (y, x),
                                                  rightAnswer=y + x)


def math2(x, y, z, i, user_id):  # 适中加减
    title_list = [['%s - %s - %s = ' % (x, y, z), x - y - z],
                  ['%s - %s + %s = ' % (x, y, z), x - y + z],
                  ['%s + %s - %s = ' % (x, y, z), x + y - z],
                  ['%s + %s + %s = ' % (x, y, z), x + y + z],
                  ['%s - (%s - %s) = ' % (x, y, z), x - (y - z)],
                  ['%s - (%s + %s) = ' % (x, y, z), x - (y + z)],
                  ['%s + (%s - %s) = ' % (x, y, z), x + (y - z)],
                  ['%s + (%s + %s) = ' % (x, y, z), x + (y + z)]]
    if x > y:
        if x - y > z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=2,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[0][0],
                                                  rightAnswer=title_list[0][1])
        else:
            if y > z:
                if x > y - z:
                    models.SelectTitleInfo.objects.create(user_id=user_id,
                                                          titleGrade=2,
                                                          titleType=0,
                                                          Course=1,
                                                          titleName=title_list[4][0],
                                                          rightAnswer=title_list[4][1]
                                                          )
                elif x > y + z:
                    models.SelectTitleInfo.objects.create(user_id=user_id,
                                                          titleGrade=2,
                                                          titleType=0,
                                                          Course=1,
                                                          titleName=title_list[5][0],
                                                          rightAnswer=title_list[5][1]
                                                          )
                else:
                    list0 = random.choice([title_list[2], title_list[6]])
                    models.SelectTitleInfo.objects.create(user_id=user_id,
                                                          titleGrade=2,
                                                          titleType=0,
                                                          Course=1,
                                                          titleName=list0[0],
                                                          rightAnswer=list0[1]
                                                          )
            else:
                if x > y + z:
                    models.SelectTitleInfo.objects.create(user_id=user_id,
                                                          titleGrade=2,
                                                          titleType=0,
                                                          Course=1,
                                                          titleName=title_list[5][0],
                                                          rightAnswer=title_list[5][1]
                                                          )
                else:
                    list1 = random.choice([title_list[1], title_list[3], title_list[7]])
                    models.SelectTitleInfo.objects.create(user_id=user_id,
                                                          titleGrade=2,
                                                          titleType=0,
                                                          Course=1,
                                                          titleName=list1[0],
                                                          rightAnswer=list1[1]
                                                          )
    else:
        if y > z:
            if x > y - z:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=2,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[4][0],
                                                      rightAnswer=title_list[4][1]
                                                      )
            else:
                list2 = random.choice([title_list[2], title_list[6]])
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=2,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=list2[0],
                                                      rightAnswer=list2[1]
                                                      )
        else:
            list3 = random.choice([title_list[3], title_list[7]])
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=2,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=list3[0],
                                                  rightAnswer=list3[1]
                                                  )


def math3(x, y, z, i, user_id):  # 偏难加减
    if x > y:
        if x - y > z:
            if i % 2 == 0:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='%s - ( ) - %s = %s' % (x, z, x - y - z),
                                                      rightAnswer=y
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='( ) - %s - %s = %s' % (y, z, x - y - z),
                                                      rightAnswer=x
                                                      )
        else:
            if i % 2 == 0:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='%s - ( ) + %s = %s' % (x, z, x - y + z),
                                                      rightAnswer=y
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='%s - %s + ( ) = %s' % (x, y, x - y + z),
                                                      rightAnswer=z
                                                      )
    else:
        if x + y > z:
            if i % 2 == 0:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='%s + %s - ( ) = %s' % (x, y, x + y - z),
                                                      rightAnswer=z
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='%s + ( ) - %s = %s' % (x, z, x + y - z),
                                                      rightAnswer=y
                                                      )
        else:
            if i % 2 == 0:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='%s + ( ) + %s = %s' % (x, z, x + y + z),
                                                      rightAnswer=y
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=3,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName='( ) + %s + %s = %s' % (y, z, x + y + z),
                                                      rightAnswer=x
                                                      )


def math4(x, y, i, user_id):  # 简单乘除
    if i % 2 == 0:
        if x != 0:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s ÷ %s = ' % (x * y, x),
                                                  rightAnswer=y
                                                  )

        else:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s × %s = ' % (x, y),
                                                  rightAnswer=x * y
                                                  )
    else:
        if y != 0:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s ÷ %s = ' % (x * y, y),
                                                  rightAnswer=x
                                                  )

        else:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName='%s × %s = ' % (y, x),
                                                  rightAnswer=x * y
                                                  )


def math5(x, y, z, i, user_id):  # 适中乘除
    title_list = [['%s ÷ %s ÷ %s = ' % (x * y * z, x, y), z], ['%s × %s × %s = ' % (x, y, z), x * y * z],
                  ['% s × % s ÷ % s = ' % (y, x * z, x), y * z], ['%s ÷ %s × %s = ' % (x * y, y, z), x * z],
                  ['%s ÷ (%s ÷ %s) = ' % (x * y * z, x * y, y), y * z], ['% s × (% s ÷ % s) = ' % (y, x * z, x), y * z],
                  ['%s ÷ (%s × %s) = ' % (x * y * z, y, z), x]]
    if i % 2 == 0:
        if x != 0 and y != 0:
            list0 = random.choice([title_list[0], title_list[4]])
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=2,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=list0[0],
                                                  rightAnswer=list0[1]
                                                  )

        else:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=2,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[1][0],
                                                  rightAnswer=title_list[1][1]
                                                  )
    else:
        if x != 0:
            list1 = random.choice([title_list[2], title_list[5]])
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=2,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=list1[0],
                                                  rightAnswer=list1[1]
                                                  )

        elif y != 0:
            if z != 0:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=2,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[6][0],
                                                      rightAnswer=title_list[6][1]
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=2,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[3][0],
                                                      rightAnswer=title_list[3][1]
                                                      )
        else:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=2,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[1][0],
                                                  rightAnswer=title_list[1][1]
                                                  )


def math6(x, y, z, i, user_id):  # 偏难乘除
    title_list = [['( ) × %s × %s = %s' % (y, z, x * y * z), x], ['%s × ( ) × %s = %s' % (x, z, x * y * z), y],
                  ['%s × %s × ( ) = %s' % (x, y, x * y * z), z], ['%s × %s ÷ ( ) = %s' % (x, y * z, x * y), z],
                  ['%s × ( ) ÷ %s = %s' % (x * z, x, y * z), y], ['( ) × %s ÷ %s = %s' % (y * z, z, x * y), x],
                  ['%s ÷ %s × ( ) = %s' % (x * y, y, x * z), z], ['%s ÷ ( ) × %s = %s' % (x * y, z, x * z), y],
                  ['( ) ÷ %s × %s = %s' % (y, z, x * z), x * y], ['( ) ÷ %s ÷ %s = %s' % (x, y, z), x * y * z],
                  ['%s ÷ ( ) ÷ %s = %s' % (x * y * z, x, z), y], ['%s ÷ %s ÷ ( ) = %s' % (x * y * z, y, z), x]]
    if x != 0 and y != 0 and z != 0:
        list0 = random.choice(title_list)
        models.SelectTitleInfo.objects.create(user_id=user_id,
                                              titleGrade=3,
                                              titleType=0,
                                              Course=1,
                                              titleName=list0[0],
                                              rightAnswer=list0[1]
                                              )
    elif x != 0 and y != 0:
        list1 = random.choice([title_list[2], title_list[6], title_list[9]])
        models.SelectTitleInfo.objects.create(user_id=user_id,
                                              titleGrade=3,
                                              titleType=0,
                                              Course=1,
                                              titleName=list1[0],
                                              rightAnswer=list1[1]
                                              )
    elif x != 0 and z != 0:
        list2 = random.choice([title_list[1], title_list[4]])
        models.SelectTitleInfo.objects.create(user_id=user_id,
                                              titleGrade=3,
                                              titleType=0,
                                              Course=1,
                                              titleName=list2[0],
                                              rightAnswer=list2[1]
                                              )
    elif y != 0 and z != 0:
        list3 = random.choice([title_list[0], title_list[5], title_list[8]])
        models.SelectTitleInfo.objects.create(user_id=user_id,
                                              titleGrade=3,
                                              titleType=0,
                                              Course=1,
                                              titleName=list3[0],
                                              rightAnswer=list3[1]
                                              )
    else:
        models.SelectTitleInfo.objects.create(user_id=user_id,
                                              titleGrade=3,
                                              titleType=0,
                                              Course=1,
                                              titleName='%s × %s × %s = ' % (x, y, z),
                                              rightAnswer=x * y * z
                                              )


def math7(x, y, z, i, user_id):  # 简单加减乘除
    title_list = [['%s + %s × %s = ' % (x, y, z), x + y * z],
                  ['%s + %s ÷ %s = ' % (x, y * z, z), x + y],
                  ['%s - %s × %s = ' % (x, y, z), x - y * z],
                  ['%s - %s ÷ %s = ' % (x, y * z, z), x - y],
                  ['%s × %s + %s = ' % (x, y, z), x * y + z],
                  ['%s × %s - %s = ' % (x, y, z), x * y - z],
                  ['%s ÷ %s + %s = ' % (x * y, y, z), x + z],
                  ['%s ÷ %s - %s = ' % (x * y, y, z), x - z]]
    if y != 0:
        if x / y > z and x > z:
            models.SelectTitleInfo.objects.create(user_id=user_id, titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[7][0],
                                                  rightAnswer=title_list[7][1]
                                                  )
        elif z != 0:
            if x > y / z and x > y:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=1,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[3][0],
                                                      rightAnswer=title_list[3][1]
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=1,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[1][0],
                                                      rightAnswer=title_list[1][1]
                                                      )
        elif x * y > z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[5][0],
                                                  rightAnswer=title_list[5][1]
                                                  )
        elif x > y * z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[2][0],
                                                  rightAnswer=title_list[2][1]
                                                  )
        else:
            list0 = random.choice([title_list[0], title_list[4], title_list[6]])
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=list0[0],
                                                  rightAnswer=list0[1]
                                                  )
    elif z != 0:
        if x > y / z and x > y:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[3][0],
                                                  rightAnswer=title_list[3][1]
                                                  )
        elif y != 0:
            if x / y > z and x > z:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=1,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[7][0],
                                                      rightAnswer=title_list[7][1]
                                                      )
            else:
                models.SelectTitleInfo.objects.create(user_id=user_id,
                                                      titleGrade=1,
                                                      titleType=0,
                                                      Course=1,
                                                      titleName=title_list[6][0],
                                                      rightAnswer=title_list[6][1]
                                                      )
        elif x * y > z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[5][0],
                                                  rightAnswer=title_list[5][1]
                                                  )
        elif x > y * z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[2][0],
                                                  rightAnswer=title_list[2][1]
                                                  )
        else:
            list0 = random.choice([title_list[0], title_list[4], title_list[1]])
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=list0[0],
                                                  rightAnswer=list0[1]
                                                  )
    else:
        if x * y > z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[5][0],
                                                  rightAnswer=title_list[5][1]
                                                  )
        elif x > y * z:
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=title_list[2][0],
                                                  rightAnswer=title_list[2][1]
                                                  )
        else:
            list0 = random.choice([title_list[0], title_list[4]])
            models.SelectTitleInfo.objects.create(user_id=user_id,
                                                  titleGrade=1,
                                                  titleType=0,
                                                  Course=1,
                                                  titleName=list0[0],
                                                  rightAnswer=list0[1]
                                                  )
