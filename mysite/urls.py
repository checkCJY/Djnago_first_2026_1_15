"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# 아래 변수는 전역변수, 변수명 수정 X
urlpatterns = [
    # 앞에는 도메인, 뒤에는 include로 앱을 호출.
    # 1번 경우
    path("polls/", include("polls.urls")),
    # http://127.0.0.1:8000/polls

    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/admin


    # 아래 코드는 메인이 polls.urls 로 설정되어짐.
    # 2번 경우
    # path('', include("polls.urls")),
    # # http://127.0.0.1:8000/

    # # 테스트
    # path('test/', include("polls.urls")), # 주소명 공백
    # # http://127.0.0.1:8000/test
    # # http://127.0.0.1:8000/test/polls, /test/test
]
