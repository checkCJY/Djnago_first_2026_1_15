from django.urls import path
from . import views

app_name = "polls"

# 아래 변수는 전역변수, 변수명 수정 X
urlpatterns = [
    # 1번 경우
    path("", views.index, name="index"),
    
    # http://127.0.0.1:8000/polls/
    # (도메인주소, views로 부터 함수 또는 클래스 호출,
    # html에서 호출될 이름)

    # 추가
    
    path("<int:question_id>/", views.detail, name="detail"),
    # http://127.0.0.1:8000/polls/question_id
    path("<int:question_id>/results/", views.results, name="results"),
    # http://127.0.0.1:8000/polls/question_id/results
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # http://127.0.0.1:8000/polls/question_id/vote/

    # # 2번 경우
    # path("", views.index, name="index"),
    # # http://127.0.0.1:8000/polls/


    # # 테스트
    # path("test", views.test, name="test"),
    # # http://127.0.0.1:8000/polls/test
]