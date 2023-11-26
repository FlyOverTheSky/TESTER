from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *

class ChoiceSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField

    class Meta:
        fields = '__all__'
        model = Choice


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set', )

    class Meta:
        fields = '__all__'
        model = Question


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='questions_set', )

    def perform_update(self):
        print(self.data)

    class Meta:
        fields = '__all__'
        model = Test


class AnswerSerializer(serializers.ModelSerializer):
    answers = serializers.JSONField()

    def validate_answers(self, answers):
        if not answers:
            raise serializers.ValidationError("Answers must be not null")
        return answers

    def save(self):
        print(self.data)
        answers = self.data['answers']
        user = self.context.user

        for question_id in answers:
            question = get_object_or_404(Question, pk=question_id)
            choices = answers[question_id]
            for choice_id in choices:
                choice = get_object_or_404(Choice, pk=choice_id)
                Answer(
                    user=user,
                    question=question,
                    choice=choice
                ).save()
                user.is_answer = True
                user.save()


class ResultSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField
    answers = AnswerSerializer(many=True, source='answer_set', )

    class Meta:
        fields = '__all__'
        model = Result
