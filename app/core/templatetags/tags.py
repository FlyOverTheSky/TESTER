from django import template
from core.models import Question

register = template.Library()


@register.filter(name='get_next_question')
def get_next_question(test_id, question_id):
    """ return next question id"""
    try:
        questions = Question.objects.filter(test_id=test_id)
        is_next = False
        for question in questions:
            if not question.is_active:
                continue
            if is_next:
                return question.id
            if question.id == question_id:
                is_next = True
    except:
        return ''


@register.filter(name='get_previous_question')
def get_previous_question(test_id, question_id):
    """ return previous question id"""
    try:
        questions = Question.objects.filter(test_id=test_id)
        previous_question = None
        for question in questions:
            if not question.is_active:
                continue
            if question.id == question_id:
                return previous_question.id
            previous_question = question
    except:
        return ''


@register.filter(name='get_first_question')
def get_first_question(test_id):
    """ return id of first_question of test. """
    try:
        questions = Question.objects.filter(test_id=test_id)
        for question in questions:
            if question.is_active:
                return question.id
    except:
        return ''
