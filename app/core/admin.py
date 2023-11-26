from django.contrib import admin

from .models import *
from .forms import *


class TestAdmin(admin.ModelAdmin):
    form = TestForm
    list_display = (
        'id',
        'title'
    )


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = (
        'text',
        'test',
        'is_active'
    )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'is_right',
        'lock_other'
    )


class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'total_result',
    )
    list_filter = ('user',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'result',
        'question',
        'choice',
        'created',
    )


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Test, TestAdmin)
