from django.db import models


# Create your models here.
class TitleStore(models.Model):  # 小学0-6年级数学题库
    createUserId = models.IntegerField('作者id', null=True)
    Class_Data = (('0', '幼儿园'), ('1', '一年级'), ('2', '二年级'), ('3', '三年级'), ('4', '四年级'), ('5', '五年级'), ('6', '六年级'))
    applyClass = models.CharField('年级', choices=Class_Data, max_length=32)
    COURSE = (('0', '语文'), ('1', '数学'), ('2', '英语'), ('3', '品德与生活'), ('4', '科学'))
    Course = models.CharField('课程', choices=COURSE, max_length=32)
    Type = (('0', '计算题'), ('1', '填空题'), ('2', '选择题'), ('3', '判断题'), ('4', '应用题'),
            ('5', '奥数题'), ('6', '阅读题'), ('7', '翻译题'), ('8', '写作题'))
    titleType = models.CharField('题目类型', choices=Type, max_length=32)
    Grade = (('0', '一般'), ('1', '适中'), ('2', '困难'), ('3', '特难'))
    titleGrade = models.CharField('难易程度', choices=Grade, default='1', max_length=30)
    titleName = models.TextField('题目问题')
    titleSubjoin = models.TextField('附加问题', null=True)  # 对题目进行补充
    titleImage = models.ImageField('附加图片', upload_to=None, height_field=None, width_field=None, max_length=100,
                                   blank=True, null=True)
    rightAnswer = models.CharField('正确答案', max_length=128)
    titleAnalysis = models.CharField('题目解析', max_length=2048, null=True)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = "小学0-6年级数学题库"
        verbose_name_plural = "小学0-6年级数学题库"

    def __str__(self):
        return self.titleName


class SelectTitleInfo(models.Model):  # 用户所选答题内容
    user_id = models.IntegerField('用户ID')
    COURSE = (('0', '语文'), ('1', '数学'), ('2', '英语'), ('3', '品德与生活'), ('4', '科学'))
    Course = models.CharField('课程', choices=COURSE, max_length=32)
    Type = (('0', '计算题'), ('1', '填空题'), ('2', '选择题'), ('3', '判断题'), ('4', '应用题'),
            ('5', '奥数题'), ('6', '阅读题'), ('7', '翻译题'), ('8', '写作题'))
    titleType = models.CharField('题目类型', choices=Type, max_length=32)
    Grade = (('0', '一般'), ('1', '适中'), ('2', '困难'), ('3', '特难'))
    titleGrade = models.CharField('难易程度', choices=Grade, default='1', max_length=30)
    titleName = models.TextField('题目问题')
    titleSubjoin = models.TextField('附加问题', null=True)  # 对题目进行补充
    titleImage = models.ImageField('附加图片', upload_to=None, height_field=None, width_field=None, max_length=100,
                                   blank=True, null=True)
    rightAnswer = models.CharField('正确答案', max_length=128)
    titleAnalysis = models.CharField('题目解析', max_length=2048, null=True)
    inputAnswer = models.CharField('输入答案', max_length=128, null=True)
    answerComparison = models.BooleanField('判断答案是否正确', null=True)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    newTime = models.DateTimeField('保存时间', auto_now=True)

    class Meta:
        verbose_name = "用户所选答题内容"
        verbose_name_plural = "用户所选答题内容"

    def __str__(self):
        return self.titleName


class AnswerInfo(models.Model):
    user_id = models.IntegerField('用户ID')
    COURSE = (('0', '语文'), ('1', '数学'), ('2', '英语'), ('3', '品德与生活'), ('4', '科学'))
    Course = models.CharField('课程', choices=COURSE, max_length=32)
    Class_Data = (('0', '幼儿园'), ('1', '一年级'), ('2', '二年级'), ('3', '三年级'), ('4', '四年级'), ('5', '五年级'), ('6', '六年级'))
    userSelectClass = models.CharField('年级', choices=Class_Data, max_length=32)
    titleCount = models.CharField('题目数量', max_length=1024)
    Grade = (('0', '一般'), ('1', '适中'), ('2', '困难'), ('3', '特难'))
    titleGrade = models.CharField('难易度', choices=Grade, default='1', max_length=30)
    submitNumber = models.IntegerField('提交结果', default='0')  # 包含【提交次数、正确个数、错误个数、错误题目及输入答案】
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    updateTime = models.DateTimeField('更新时间', auto_now=True)
    startTime = models.IntegerField('开始时间', null=True)
    endTime = models.IntegerField('结束时间', null=True)

    class Meta:
        verbose_name = '答题信息'
        verbose_name_plural = '答题信息'

    def __str__(self):
        return self.titleCount
