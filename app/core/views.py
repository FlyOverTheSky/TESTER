from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import ChoicesForm


User = get_user_model()
# TODO: После выбора ответа, ответ сохраняется, но не отображается в форме.


class TestListView(LoginRequiredMixin, ListView):
    """ View-класс для главной страницы с тестами. """
    model = Test
    ordering = 'id'
    paginate_by = 50


class AllResultsView(LoginRequiredMixin, ListView):
    """ View-класс для главной страницы с тестами. """
    model = Result
    ordering = 'user'
    paginate_by = 50


@login_required
def question_view(request, test_id, question_id):
    """ View-функция для обработки каждого вопроса отдельно. """
    test = get_object_or_404(Test, pk=test_id)
    current_question = Question.objects.get(test_id=test_id, id=question_id)
    choices = Choice.objects.filter(question_id=question_id)
    choices_form = ChoicesForm(question_id)
    if request.method == 'POST':
        # Если есть незавершенная попытка у пользователя с конкретным тестом, то переопределяем в нем данные
        # Если незавершенной попытки нет, то создаем новую.
        result = Result.objects.get_or_create(
            test=test,
            user=request.user,
            is_finished=False,
        )[0]
        choice_number = request.POST.get('choice')
        # Проверка на наличие выбора.
        if choice_number:
            choice_number = int(choice_number)
            # Если уже создавался объект Answer в этой попытке, то обновляем выбор
            # Если еще не давался ответ на вопрос, то создаем объект Answer
            selected_choice = Choice.objects.get(id=choice_number)
            answer = Answer.objects.update_or_create(
                result=result,
                question=current_question,
                defaults={
                    'choice': selected_choice,
                    'is_right': selected_choice.is_right
                }
            )

    context = {
        'test': test,
        'question': current_question,
        'choices': choices,
        'choices_form': choices_form,
    }
    return render(request, 'core/question.html', context)


@login_required
def test_result(request, test_id):
    result = get_object_or_404(
        Result,
        test_id=test_id,
        user=request.user,
        is_finished=False
    )
    answers = Answer.objects.filter(result_id=result.id)
    total_answers = len(answers)
    questions = Question.objects.filter(test_id=test_id, is_active=True)
    if total_answers != len(questions):
        for question in questions:
            for answer in answers:
                if answer.question_id == question.id:
                    break
            else:
                return question_view(request, result.test_id, question.id)

    right_answers = answers.filter(is_right=True)
    total_right_answers = len(right_answers)
    percent = int((total_right_answers/total_answers) * 100)
    context = {
        'total_answers': total_answers,
        'total_right_answers': total_right_answers,
        'percent': percent,
    }
    result.total_result = percent
    result.is_finished = True
    result.save()
    return render(request, 'core/result.html', context)
