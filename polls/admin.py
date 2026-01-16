from django.contrib import admin
from .models import Question, Choice    # 추가

admin.site.register(Question)
admin.site.register(Choice) # 추가
