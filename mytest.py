from collections import Counter

# math = ['5']
# for num in math:
#     if int(num) == 1:
#         print('aa')
#     elif int(num) == 2:
#         print('bbb')
#     elif int(num) == 3:
#         print('ccc')
#     else:
#         print('null')

# a = ['1', '2', '2', '3']
# b = ['1', '2', '3']
#
# print(len(set(a).intersection(set(b))))
# print((50 / 2) % 2)
# print(Counter(a)['2'])

# import time
#
# print('按下回车开始计时，按下 Ctrl + C 停止计时。')
# while True:
#
#     input("")  # 如果是 python 2.x 版本请使用 raw_input()
#     starttime = time.time()
#     print('开始')
#     try:
#         while True:
#             print('计时: ', round(time.time() - starttime, 0), '秒', end="\r")
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print('结束')
#         endtime = time.time()
#         print('总共的时间为:', round(endtime - starttime, 2), 'secs')
#         break


# a = {'a': 1, 'b': 2}
# print('c' in a)

# a = [1, 2, 5, 9]
# for b in a:
#     for c in a:
#         if c != b:
#             print(c + b)


# import random
#
# list1 = ['佛山', '南宁', '北海', '杭州', '南昌', '厦门', '温州']
# a = random.choice(list1)
# print(a)


# from PIL import Image
# import numpy as np
#
# a = Image.open("fromimg.png")
# a.show()
# b = a.resize((300, 300))
# datab = list(b.getdata())
# # print type(datab)
# obj1 = []
# obj2 = []
# for i in range(len(datab)):
#     obj1.append([sum(datab[i]) / 3])  # 灰度化方法1：RGB三个分量的均值
#     obj2.append([0.3 * datab[i][0] + 0.59 * datab[i][1] + 0.11 * datab[i][2]])
#     # 灰度化方法2：根据亮度与RGB三个分量的对应关系：Y=0.3*R+0.59*G+0.11*B
#
# obj1 = np.array(obj1).reshape((300, 300))
# obj2 = np.array(obj2).reshape((300, 300))
# print(obj1)
# print(obj2)
#
# arrayimg1 = Image.fromarray(obj1)
# arrayimg2 = Image.fromarray(obj2)
# arrayimg1.show()
# arrayimg2.show()
#
#
# from PIL import Image, ImageDraw
#
#
# def synthesis_image(mother_img, son_img, save_img, coordinate=None):
#     # 将图片赋值,方便后面的代码调用
#     M_Img = Image.open(mother_img)
#     S_Img = Image.open(son_img)
#     factor = 2  # 子图缩小的倍数1代表不变，2就代表原来的一半
#
#     # 给图片指定色彩显示格式
#     M_Img = M_Img.convert("RGBA")  # CMYK/RGBA 转换颜色格式（CMYK用于打印机的色彩，RGBA用于显示器的色彩）
#
#     # 获取图片的尺寸
#     M_Img_w, M_Img_h = M_Img.size  # 获取被放图片的大小（母图）
#     print("母图尺寸：", M_Img.size)
#     S_Img_w, S_Img_h = S_Img.size  # 获取小图的大小（子图）
#     print("子图尺寸：", S_Img.size)
#
#     size_w = int(S_Img_w / factor)
#     size_h = int(S_Img_h / factor)
#
#     # 防止子图尺寸大于母图
#     if S_Img_w > size_w:
#         S_Img_w = size_w
#     if S_Img_h > size_h:
#         S_Img_h = size_h
#
#     # # 重新设置子图的尺寸
#     icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
#     # icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
#     w = int((M_Img_w - S_Img_w) / 2)
#     h = int((M_Img_h - S_Img_h) / 2)
#
#     try:
#         if coordinate == None or coordinate == "":
#             coordinate = (w, h)
#             # 粘贴子图到母图的指定坐标（当前居中）
#             M_Img.paste(icon, coordinate, mask=None)
#         else:
#             print("已经指定坐标")
#             # 粘贴子图到母图的指定坐标（当前居中）
#             M_Img.paste(icon, coordinate, mask=None)
#     except:
#         print("坐标指定出错 ")
#     # 保存图片
#     M_Img.save(save_img)
#     M_Img.show(save_img)
#
#
# def new_image(width, height, color='#CCFFCC'):  # 生成空的图片模板
#     img = Image.new('RGBA', (int(width), int(height)), color)
#     img.save('text_None.png')
#     print(img.size)
#     return img
#
#
# def new_im(mother_img):
#     im = Image.open(mother_img)
#     draw = ImageDraw.Draw(im)  # 实例化一个对象
#     for i in range(im.size[1] - 428):
#         if i % 2 == 0:
#             # print('偶数', i)
#             draw.line((im.size[0] / 2, i + 541) + (im.size[0] / 2, i + 545), fill=(0, 0, 128))  # 线的起点和终点，线宽
#         else:
#             # print(i)
#             draw.line((im.size[0] / 2, i + 541) + (im.size[0] / 2, i + 545))
#     # draw.line((0, im.size[1], im.size[0], 0))
#     # draw.line((193, 0) + , fill=128, width=5)
#     im.show()
#
#
# if __name__ == '__main__':
#     new_image(386, 800, color='#EFD07D')
#
#     synthesis_image(mother_img="text_None.png",
#                     son_img="test2.png",
#                     save_img="test.png",
#                     # coordinate=None  # 如果为None表示直接将子图在母图中居中也可以直接赋值坐标
#                     coordinate=(0, 586)
#                     )
#     synthesis_image(mother_img="test.png",
#                     son_img="testtop.png",
#                     save_img="test0.png",
#                     # coordinate=None  # 如果为None表示直接将子图在母图中居中也可以直接赋值坐标
#                     coordinate=(0, 0)
#                     )
#     new_im(mother_img="test0.png")

# import time
#
# print(int(time.time()))
# t = time.localtime(time.time())
# print(t)
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

# import math
#
# totalTime = 20
# if totalTime <= 60:  # 秒
#     print(totalTime)
# elif 60 < totalTime <= 60 * 60:  # 分
#     m = math.modf(totalTime / 60)
#     print('%s分%s秒' % (math.ceil(m[1]), math.ceil(m[0] * 60)))
# elif 60 * 60 < totalTime <= 60 * 60 * 24:  # 时
#     h = math.modf(totalTime / 3600)
#     m = math.modf(h[0] * 60)
#     print('%s时%s分%s秒' % (math.ceil(h[1]), math.ceil(m[1]), math.ceil(m[0] * 60)))
# else:
#     t = math.modf(totalTime / (3600 * 24))
#     h = math.modf(t[0] * 24)
#     m = math.modf(h[0] * 60)
#     print('%s天%s时%s分%s秒' % (math.ceil(t[1]), math.ceil(h[1]), math.ceil(m[1]), math.ceil(m[0] * 60)))
# import random
#
# l = [["mathTitle='( ) ÷ %s ÷ %s = %s' % (x, y, z)", "mathResult = x * y * z"],
#      ["mathTitle='%s ÷ ( ) ÷ %s = %s' % (x * y * z, x, z)", "mathResult=y"],
#      ["mathTitle='%s ÷ %s ÷ ( ) = %s' % (x * y * z, y, z)", "mathResult=x"]]
# l2 = [l[0], l[2]]
# print(random.choice(l)[0], random.choice(l)[1])
# print(l2)


# l = [{'mathTitle': '15 × 160 ÷ 10 = '}, {'mathTitle': '3040 ÷ 8 ÷ 19 = '}, {'mathTitle': '0 × 33 ÷ 3 = '},
#      {'mathTitle': '119 ÷ 17 ÷ 7 = '}, {'mathTitle': '16 × 66 ÷ 6 = '}, {'mathTitle': '374 ÷ 17 ÷ 11 = '},
#      {'mathTitle': '4 × 12 ÷ 1 = '}, {'mathTitle': '1296 ÷ 9 ÷ 12 = '}, {'mathTitle': '20 × 200 ÷ 20 = '},
#      {'mathTitle': '9 × ( ) ÷ 3 = 3'}, {'mathTitle': '( ) ÷ 10 ÷ 18 = 5'}, {'mathTitle': '11 × ( ) ÷ 9 = 99'},
#      {'mathTitle': '( ) ÷ 2 ÷ 0 = 6'}, {'mathTitle': '72 × ( ) ÷ 6 = 54'}, {'mathTitle': '( ) ÷ 9 ÷ 2 = 15'},
#      {'mathTitle': '15 × ( ) ÷ 2 = 6'}, {'mathTitle': '( ) ÷ 20 ÷ 12 = 4'}, {'mathTitle': '180 × ( ) ÷ 10 = 100'},
#      {'mathTitle': '( ) ÷ 11 ÷ 4 = 6'}, {'mathTitle': '7 × ( ) ÷ 6 = 42'}]
# ll = [{'mathResult': '240'}, {'mathResult': '20'}, {'mathResult': '0'}, {'mathResult': '1'}, {'mathResult': '176'},
#       {'mathResult': '2'}, {'mathResult': '48'}, {'mathResult': '12'}, {'mathResult': '200'}, {'mathResult': '9'},
#       {'mathResult': '900'}, {'mathResult': '1'}, {'mathResult': '0'}, {'mathResult': '8'}, {'mathResult': '270'},
#       {'mathResult': '5'}, {'mathResult': '960'}, {'mathResult': '18'}, {'mathResult': '264'}, {'mathResult': '1'}]
# for i in range(len(l)):
#     print(l[i]['mathTitle']+'==========='+ll[i]['mathResult'])

# python - 字符串指定位置插入字符
# def insertStr():
#     # 有一个字符串
#     str_1 = '（）+2=5'
#     # 把字符串转为 list
#     str_list = list(str_1)
#     # 字符数， 可以利用这个在某个位置插入字符
#     # count = len(str_list)
#     # 找到 斜杠的位置
#     nPos = str_list.index('）')
#     # 在斜杠位置之前 插入要插入的字符
#     str_list.insert(nPos, '3')
#     # 将 list 转为 str
#     str_2 = "".join(str_list)
#     print(str_2)
#
#
# if __name__ == '__main__':
#     insertStr()

# list0 = [{'mathNewResult': '25'}, {'mathNewResult': None}, {'mathNewResult': None}]
# for i in list0:
#     print(i)
#     if i.get('mathNewResult', None) == 0:
#         print('T')
#     else:
#         print('F')
# txt_list = []
# with open('topic.txt', 'r', encoding='UTF-8') as f:
#     for data in f.readlines():
#         if len(data.split('.')) > 1:
#             txt_list.append({'id': data.split('.')[0].strip(), 'title': data.split('.')[1].strip(), 'answer': ''})
# print(txt_list)


# s = '123456'
# print(len(s))

# a = []
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         b = "%d*%d=%d" % (j, i, j * i)
#         print(b)
#         a.append(b)
#     # print("")
# print(a)


# a = ['12', '14', '15']
# b = ['1', '2']
# if b == a:
#     print('1')
# else:
#     print('0')

# sstr = """['0', '842', '17423', '34216', '74222', '92483']"""
# a = sstr.split("#")
# b = eval(sstr)
# print(b)

# str_1 = 'wo shi yi zhi da da niu '
# char_1 = 'i'
# nPos = str_1.find(char_1)
# print(nPos)

# 开挂模式
# str_1 = '100里面有()个一，()个十()。'
# # char_1 = '('
# # count = 0
# l_list = ['100', '10', '0']
# # str_list = list(str_1)
# # print(str_list)
# # print(str_1.count('()'))
# # print(str_1.replace('()', '1', 1))
# for i in range(str_1.count('()')):
#     str_1 = str_1.replace('()', l_list[i], 1)
# print(str_1)

# import ast
# a = "{'count': {'Type': '0', 'mathType': '1', 'mathCount': '10', 'numberRange': '20', 'mathGrade': '2'}, 'fill': {'Type': '1', 'mathFill': '10'}, 'choose': {'Type': '2', 'mathCoose': '10'}, 'verdict': {'Type': '3', 'mathVerdict': '5'}, 'use': {'Type': '4', 'mathUse': '5'}, 'number': {'Type': '5', 'mathNumber': '2'}}"
# udict = ast.literal_eval(a)
# print(type(udict))


# verdict_list = []
# with open('bank/verdict.txt', 'r', encoding='UTF-8') as f:
#     for data in f.readlines():
#         # if len(data.split('.')) > 1:
#         #     verdict_list.append({'title': data.split('.')[0].strip(), 'answer': data.split('.')[1].strip(),
#         #                          'Analysis': data.split('.')[2].strip()})
#         print('判断题:', len(data.split('.')))
# # print('判断题:', verdict_list)

# def index_class(request):
#     user_id = request.session.get('_auth_user_id')
#     user_profile = UserProfile.objects.get(user_id=user_id)
#     num_list = Math.objects.filter(user_id=user_id).order_by('mathClass').all()
#     num_info_list = MathTypeinfo.objects.get(user_id=user_id)
#     math_count_dict = ast.literal_eval(num_info_list.mathCount)
#     # print(math_count_dict['fill']['mathFill'])
#     num = Math.objects.filter(user_id=user_id).order_by('mathClass')[:2]  # 随机从数据库取出指定条数的数据
#     print(num)
#
#     # 应用题
#     use1_list = []
#     with open('bank/use1.txt', 'r', encoding='UTF-8') as f:
#         for data in f.readlines():
#             if len(data.split('.')) > 1:
#                 # models.TitleInfo.objects.create(userClass=user_profile.userClass,
#                 #                                 titleType='4',
#                 #                                 titleName=data.split('.')[1].strip(),
#                 #                                 titleAnswer=data.split('.')[2].strip())
#                 use1_list.append(
#                     {'id': data.split('.')[0].strip(), 'title': data.split('.')[1].strip(),
#                      'answer': data.split('.')[2].strip()})
#     print('应用题:', use1_list)
#
#     # 填空题
#     filling_list = []
#     name_list = []
#     with open('bank/filling.txt', 'r', encoding='UTF-8') as f:
#         for data in f.readlines():
#             # print(data.split('.'))
#             if len(data.split('.')) > 1:
#                 # models.TitleInfo.objects.create(userClass=user_profile.userClass,
#                 #                                 titleType='1',
#                 #                                 titleName=data.split('.')[1].strip(),
#                 #                                 titleAnswer=data.split('.')[2].strip().split(','))
#                 filling_list.append({'id': data.split('.')[0].strip(),
#                                      'name': data.split('.')[1].strip().replace('()',
#                                                                                 '<input name="1" style="width:50px;"/>')})
#                 name_list.append(data.split('.')[1].strip().replace('()', '<input style="width:50px;"/>'))
#     print('填空题:', filling_list)
#     print('填空题:', name_list)
#
#     # 选择题
#     select_list = []
#     with open('bank/select.txt', 'r', encoding='UTF-8') as f:
#         for data in f.readlines():
#             if len(data.split('.')) > 1:
#                 # models.TitleInfo.objects.create(userClass=user_profile.userClass,
#                 #                                 titleType='2',
#                 #                                 titleName={'title': data.split('。')[0].strip(),
#                 #                                            'select': data.split('。')[1].strip()},
#                 #                                 titleImage='',
#                 #                                 titleAnswer=data.split('。')[2].strip())
#                 select_list.append(
#                     {'title': data.split('.')[1].strip().replace('()', '<input name="1" style="width:50px;"/>'),
#                      'select': data.split('.')[2].strip(),
#                      'answer': data.split('.')[3].strip()})
#     print('选择题:', select_list)
#
#     # 判断题
#     verdict_list = []
#     with open('bank/verdict.txt', 'r', encoding='UTF-8') as f:
#         for data in f.readlines():
#             if len(data.split('.')) > 1:
#                 # models.TitleInfo.objects.create(userClass=user_profile.userClass,
#                 #                                 titleType='3',
#                 #                                 titleName=data.split('.')[0].strip(),
#                 #                                 titleImage='',
#                 #                                 titleAnswer=data.split('.')[1].strip(),
#                 #                                 titleAnalysis=data.split('.')[2].strip())
#                 verdict_list.append({'title': data.split('.')[0].strip(), 'answer': data.split('.')[1].strip(),
#                                      'Analysis': data.split('.')[2].strip()})
#             # print('判断题:', data.split('.'))
#     print('判断题:', verdict_list)
#
#     # 奥数题
#     number_list = []
#     with open('bank/number.txt', 'r', encoding='UTF-8') as f:
#         for data in f.readlines():
#             if len(data.split('.')) > 1:
#                 # models.TitleInfo.objects.create(userClass=user_profile.userClass,
#                 #                                 titleType='5',
#                 #                                 titleName=data.split('.')[1].strip(),
#                 #                                 titleImage='',
#                 #                                 titleAnswer='')
#                 number_list.append({'title': data.split('.')[1].strip()})
#     print('奥数题:', number_list)
#
#     return render(request, 'index.html',
#                   {'num': num_list,
#                    'name_list': name_list,
#                    'menu': random.sample(use1_list, int(math_count_dict['use']['mathUse'])),
#                    'filling_list': random.sample(filling_list, int(math_count_dict['fill']['mathFill'])),
#                    'select_list': random.sample(select_list, int(math_count_dict['select']['mathSelect']))})
# import random

# a = ['1', '1', '3', 'd', 'f', 'g']
# print(random.sample(a, 3))
# for i in enumerate(a):
#     print(i)
# print(len(Counter(a)))
# b = len(Counter(a))
# for i in range(b):
#     print(i+1)

import jieba
ss = "你是想红寺湖但行好事时尚先生"
print(jieba.lcut(ss))
print(jieba.lcut_for_search(ss))

s = '你'

if s in jieba.lcut_for_search(ss):
    print('True')
