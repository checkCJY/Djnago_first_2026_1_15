from django.urls import path
from . import views

app_name = "polls"

# 아래 변수는 전역변수, 변수명 수정 X
urlpatterns = [
    # (도메인주소, views로 부터 함수 또는 클래스 호출,
    # html에서 호출될 이름)

    # http://127.0.0.1:8000/polls/
    # path("", views.index, name="index"),
    path("", views.IndexView.as_view(), name="index"),

    # 추가
    # http://127.0.0.1:8000/polls/question_id
    # path("<int:question_id>/", views.detail, name="detail"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    
    # http://127.0.0.1:8000/polls/question_id/results
    # path("<int:question_id>/results/", views.results, name="results"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),

    # http://127.0.0.1:8000/polls/question_id/vote
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    # path("aa/", views.aa, name="aa"),
    # http://127.0.0.1:8000/polls/aa
]