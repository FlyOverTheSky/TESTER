from django.urls import path

from .views import *


app_name = 'core'

urlpatterns = [
    path('', TestListView.as_view(), name='test_list'),
    path('tests/test_<int:test_id>/question_<int:question_id>', question_view, name='questions'),
    path('result/result_of_test_<int:test_id>', test_result, name='test_result'),
    path('result_list', AllResultsView.as_view(), name='result_list')
]