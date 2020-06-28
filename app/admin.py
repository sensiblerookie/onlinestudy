from django.contrib import admin
from app.models import TitleStore, SelectTitleInfo, AnswerInfo


# Register your models here.

class TitleStoreAdmin(admin.ModelAdmin):
    list_display = ['createUserId', 'applyClass', 'Course', 'titleType', 'titleGrade', 'titleName',
                    'titleSubjoin', 'titleImage', 'rightAnswer', 'titleAnalysis', 'createTime']


class SelectTitleInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'Course', 'titleType', 'titleGrade', 'titleName', 'titleSubjoin', 'titleImage',
                    'rightAnswer', 'titleAnalysis', 'inputAnswer', 'answerComparison', 'createTime', 'newTime']


class AnswerInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'Course', 'userSelectClass', 'titleCount', 'titleGrade', 'submitNumber',
                    'createTime', 'updateTime', 'startTime', 'endTime']


admin.site.register(TitleStore, TitleStoreAdmin)
admin.site.register(SelectTitleInfo, SelectTitleInfoAdmin)
admin.site.register(AnswerInfo, AnswerInfoAdmin)
