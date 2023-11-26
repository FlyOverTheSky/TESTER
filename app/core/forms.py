from django import forms
from .models import *


class TestForm(forms.ModelForm):
    def clean(self):
        is_active = self.data.get('is_active')
        if is_active:

            # Костыль, тк возникала ошибка при попытке сделать тест сразу активным при создании
            try:
                current_test = Test.objects.get(title=self.data['title'])
            except Test.DoesNotExist:
                raise forms.ValidationError({'is_active': 'Должен быть хотя бы один вопрос в тесте!'})

            questions = Question.objects.filter(test_id=current_test.id)
            if not questions:
                raise forms.ValidationError({'is_active': 'Должен быть хотя бы один вопрос в тесте!'})

    class Meta:
        model = Test
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    def clean(self):
        is_active = self.data.get('is_active')
        if is_active:

            # Костыль, тк возникала ошибка при попытке сделать вопрос сразу активным при создании
            try:
                current_question = Question.objects.get(text=self.data['text'])
            except Question.DoesNotExist:
                raise forms.ValidationError({'text': 'Должен быть хотя бы один вариант ответа!'})

            choices = Choice.objects.filter(question_id=current_question.id)

            if not choices:
                raise forms.ValidationError({'text': 'Должен быть хотя бы один вариант ответа!'})

            have_answer = False
            right_answers = 0
            for choice in choices:
                if choice.is_right:
                    have_answer = True
                    right_answers += 1

            if right_answers == len(choices):
                raise forms.ValidationError({'is_active': 'Все ответы не могут быть правильными!'})

            if not have_answer:
                raise forms.ValidationError({'is_active': 'У вопроса нет правильного ответа!'})

    class Meta:
        model = Question
        fields = '__all__'


class ChoicesForm(forms.Form):
    choice_field = forms.ChoiceField(
            choices=(),
            label=False,
            widget=forms.Select(attrs={
                'style': 'border-color: white; outline:none; width: 140px'
            })
        )

    def __init__(self, question_id):
        super(ChoicesForm, self).__init__(question_id)
        choices = list(Choice.objects.filter(question_id=question_id))
        for i in choices:
            self.fields['choices_fields'] = choices
