from django.urls import path
from . import views
from . import practice_views

app_name = "polls"

# 아래 변수는 전역변수, 변수명 수정 X
urlpatterns = [
    # (도메인주소, views로 부터 함수 또는 클래스 호출,
    # html에서 호출될 이름)

    # http://127.0.0.1:8000/polls/
    # http://127.0.0.1:8000/polls/question_id
    # http://127.0.0.1:8000/polls/question_id/results
    # http://127.0.0.1:8000/polls/question_id/vote

    # FBV
    # path("", views.index, name="index"),
    # path("<int:question_id>/", views.detail, name="detail"),
    # path("<int:question_id>/results/", views.results, name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),

    # CBV
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    
    # CRUD

    path("create/", views.QuestionCreateView.as_view(), name="question_create"),
    # http://127.0.0.1:8000/polls/create
    # 제너릭에 CreateView 상속받아서 클래스 글 생성을 구현
    # url polls:question_create 탬플릿(html)에서 링크 형태로 호출


    path("<int:pk>/update/", views.QuestionUpdateView.as_view(), name="question_update"),
    # http://127.0.0.1:8000/polls/id/update
    # 제너릭에 UpdateView 상속받아서 클래스 글 생성을 구현
    # url polls:question_update 탬플릿(html)에서 링크 형태로 호출

    path("<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="question_delete"),
    # http://127.0.0.1:8000/polls/id/delete
    # 제너릭에 DeleteView 상속받아서 클래스 글 생성을 구현
    # url polls:question_delete 탬플릿(html)에서 링크 형태로 호출

    # # practice_id
    # path("practice/1/", practice_views.practice_1, name="practice_1"),
    # # http://127.0.0.1:8000/polls/practice/1/?q=~~~

    # path("practice/2/", practice_views.practice_2, name="practice_2"),
    # # http://127.0.0.1:8000/polls/practice/2/?q=~~~

    # path("practice/3/", practice_views.practice_3, name="practice_3"),
    # # http://127.0.0.1:8000/polls/practice/3/?show=~~~


    # # practice_api
    # path("practice/api/1/", practice_views.practice_api_1, name="practice_api_1"),
    # # http://127.0.0.1:8000/polls/practice/api/1/?q=~~~

    # path("practice/api/2/", practice_views.practice_api_2, name="practice_api_2"),
    # # http://127.0.0.1:8000/polls/practice/api/2/?q=~~~

    # path("practice/api/3/", practice_views.practice_api_3, name="practice_api_3"),
    # # http://127.0.0.1:8000/polls/practice/api/2/?show=~~~

    path('practice/', practice_views.practice_index, name='practice_index'),

    # 연습 1
    path('practice-1/', practice_views.practice_1, name='practice_1'),
    path('practice-api-1/', practice_views.practice_api_1, name='practice_api_1'),
    
    # 연습 2
    path('practice-2/', practice_views.practice_2, name='practice_2'),
    path('practice-api-2/', practice_views.practice_api_2, name='practice_api_2'),
    
    # 연습 3
    path('practice-3/', practice_views.practice_3, name='practice_3'),
    path('practice-api-3/', practice_views.practice_api_3, name='practice_api_3'),

    # 연습 5 
    path('practice-5/', practice_views.practice_5, name='practice_5'),
    path('practice-api-5/', practice_views.practice_api_5, name='practice_api_5'),

    # 연습 6
    path('practice-6/', practice_views.practice_6, name='practice_6'),
    path('practice-api-6/', practice_views.practice_api_6, name='practice_api_6'),

]