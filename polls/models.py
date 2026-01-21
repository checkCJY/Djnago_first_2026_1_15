from django.db import models


class Question(models.Model):
	# 각각 변수에 
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

	# 객체를 문자열로 표현할 때 (관리자 페이지 등에서 유용)
    # def __str__(self):
    #     return self.question_text
    def __str__(self):
        return f"{self.id} - {self.question_text} - {self.pub_date}"
    
    # 테스트코드와 연관
    # 논리적, 정확히 떨어져야 하는 경우에 테스트코드 작성
    # 연산, 비교함수 들어가므로
    def was_published_recently(self):
        from django.utils import timezone
        import datetime
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # 리턴값 복붙해서 변경안했더니 오류발생
    # 항상 출력으로 뭘 줄지 생각을하자.
    def __str__(self):
        return self.choice_text