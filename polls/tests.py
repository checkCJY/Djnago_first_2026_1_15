# 개선 후 테스트 코드
import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from .models import Question
from django.contrib.auth.models import User


# 공통함수(변경없음)
def create_question(question_text, days):
    """
    days: 질문 공개 날짜(pub_date)를 오늘 기준으로 며칠 전/후로 설정
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text, 
        pub_date=time
        )


# 모델 메서드 테스트(변경됨)
class QuestionModelTests(TestCase):
    def setUp(self):
        """
        매 테스트마다 사용할 기본 질문 객체 3종 생성
        """
        now = timezone.now()
        self.future_question = Question(pub_date=now + datetime.timedelta(days=30))
        self.old_question = Question(pub_date=now - datetime.timedelta(days=1, seconds=1))
        self.recent_question = Question(pub_date=now - datetime.timedelta(hours=23, minutes=59, seconds=59))

    def test_was_published_recently_with_future_question(self):
        """미래 질문은 최근 게시된 것이 아니므로 False"""
        self.assertIs
        (self.future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """1일 이상 지난 과거 질문은 False"""
        self.assertIs
        (self.old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """24시간 이내의 질문은 True"""
        self.assertIs
        (self.recent_question.was_published_recently(), True)

# 수정코드, polls/views.py 코드
class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.url = reverse("polls:index")
    
    def _get_questions_from_response(self, url_params=''):
        """헬퍼: URL 요청 후 질문 리스트 반환"""
        response = self.client.get(self.url + url_params)
        self.assertEqual(response.status_code, 200)
        return list(response.context["latest_question_list"])
    
    def _assert_questions_equal(self, url_params, expected_questions):
        """헬퍼: URL 파라미터로 요청 후 질문 목록 검증"""
        questions = self._get_questions_from_response(url_params)
        self.assertEqual(questions, expected_questions)
    
    # 기존 테스트
    def test_no_questions(self):
        response = self.client.get(self.url)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        q = create_question("Past question", days=-30)
        self._assert_questions_equal('', [q])

    def test_future_question(self):
        create_question("Future question", days=30)
        response = self.client.get(self.url)
        self.assertContains(response, "No polls are available.")

    def test_future_question_and_past_question(self):
        past = create_question("Past question", days=-30)
        create_question("Future question", days=30)
        self._assert_questions_equal('', [past])

    def test_two_past_questions(self):
        q1 = create_question("Past question 1", days=-30)
        q2 = create_question("Past question 2", days=-5)
        self._assert_questions_equal('', [q2, q1])
    
    # 새로운 필터 테스트
    def test_search_filter(self):
        q1 = create_question("SQL 배우기", days=-1)
        create_question("Django 배우기", days=-2)
        
        questions = self._get_questions_from_response('?q=SQL')
        self.assertIn(q1, questions)
        self.assertEqual(len(questions), 1)
    
    def test_date_start_filter(self):
        old = create_question("오래된 질문", days=-10)
        recent = create_question("최근 질문", days=-1)
        
        start = (timezone.now() - datetime.timedelta(days=5)).date()
        questions = self._get_questions_from_response(f'?start={start}')
        
        self.assertIn(recent, questions)
        self.assertNotIn(old, questions)
    
    def test_date_end_filter(self):
        old = create_question("오래된 질문", days=-10)
        recent = create_question("최근 질문", days=-1)
        
        end = (timezone.now() - datetime.timedelta(days=5)).date()
        questions = self._get_questions_from_response(f'?end={end}')
        
        self.assertIn(old, questions)
        self.assertNotIn(recent, questions)
    
    def test_order_oldest(self):
        q1 = create_question("질문 1", days=-10)
        q2 = create_question("질문 2", days=-1)
        
        self._assert_questions_equal('?order=oldest&show=future', [q1, q2])


class QuestionDetailViewTests(TestCase):
    def _get_detail_response(self, question):
        """헬퍼: 질문 상세 페이지 응답 반환"""
        url = reverse("polls:detail", args=(question.id,))
        return self.client.get(url)
    
    def test_future_question(self):
        future = create_question("Future question", days=5)
        response = self._get_detail_response(future)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past = create_question("Past question", days=-5)
        response = self._get_detail_response(past)
        self.assertContains(response, past.question_text)


class VoteViewTests(TestCase):
    def setUp(self):
        self.question = create_question("투표 질문", days=-1)
        self.choice = self.question.choice_set.create(choice_text="선택 1")
        self.url = reverse('polls:vote', args=(self.question.id,))
    
    def _vote(self, choice_id=None):
        """헬퍼: 투표 요청"""
        data = {'choice': choice_id} if choice_id else {}
        return self.client.post(self.url, data)
    
    def test_vote_success(self):
        response = self._vote(self.choice.id)
        
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
    
def test_vote_without_choice(self):
    response = self._vote()
    self.assertEqual(response.status_code, 200)  # 에러 페이지 렌더링됨
    self.assertIn('error_message', response.context)  # 컨텍스트에 에러 있음

def test_vote_invalid_choice(self):
    response = self._vote(99999)
    self.assertEqual(response.status_code, 200)
    self.assertIn('error_message', response.context)


class QuestionCRUDTests(TestCase):
    def _create_question_data(self, text="새 질문"):
        """헬퍼: 질문 생성/수정용 데이터"""
        return {
            'question_text': text,
            'pub_date': timezone.now(),
        }
    
    def test_create_get(self):
        response = self.client.get(reverse('polls:question_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/question_form.html')
    
    def test_create_post(self):
        response = self.client.post(
            reverse('polls:question_create'),
            self._create_question_data('새로운 질문')
        )
        
        self.assertEqual(Question.objects.count(), 1)
        self.assertRedirects(response, reverse('polls:index'))
        self.assertEqual(Question.objects.first().question_text, '새로운 질문')
    
    def test_update(self):
        q = create_question("원래", days=-1)
        
        response = self.client.post(
            reverse('polls:question_update', args=(q.id,)),
            self._create_question_data('수정됨')
        )
        
        q.refresh_from_db()
        self.assertEqual(q.question_text, '수정됨')
        self.assertRedirects(response, reverse('polls:detail', args=(q.id,)))
    
    def test_delete(self):
        q = create_question("삭제", days=-1)
        
        response = self.client.post(reverse('polls:question_delete', args=(q.id,)))
        
        self.assertEqual(Question.objects.count(), 0)
        self.assertRedirects(response, reverse('polls:index'))

# account/views.py 로직검사
class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        # 공통으로 사용할 유효한 비밀번호
        self.valid_password = 'testpass123!@#'


        # 테스트용 Question 데이터 생성
        self.q1 = Question.objects.create(
            question_text="SQL 배우기",
            pub_date=timezone.now() - datetime.timedelta(days=1)
        )
        self.q2 = Question.objects.create(
            question_text="Django 배우기",
            pub_date=timezone.now() + datetime.timedelta(days=1)
        )
    
    def _create_signup_data(self, username='testuser', password1=None, password2=None):
        """회원가입 데이터 생성 헬퍼 메서드"""
        return {
            'username': username,
            'password1': password1 or self.valid_password,
            'password2': password2 or self.valid_password,
        }
    
    def _assert_signup_failed(self, response, username):
        """회원가입 실패 공통 검증"""
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertTrue(response.context['form'].errors)
    
    def test_signup_get_request(self):
        """GET 요청 시 회원가입 폼이 렌더링되는지 테스트"""
        response = self.client.get(self.signup_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIn('form', response.context)
    
    def test_signup_post_valid_data(self):
        """유효한 데이터로 회원가입 성공 테스트"""
        username = 'testuser'
        data = self._create_signup_data(username)
        
        response = self.client.post(self.signup_url, data)
        
        # 리다이렉트 및 유저 생성 확인
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())
        
        # 성공 메시지 확인
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn('회원가입이 완료되었습니다', str(messages[0]))
    
    def test_signup_post_password_mismatch(self):
        """비밀번호 불일치 시 회원가입 실패 테스트"""
        username = 'testuser2'
        data = self._create_signup_data(
            username=username,
            password2='differentpass123!@#'
        )
        
        response = self.client.post(self.signup_url, data)
        self._assert_signup_failed(response, username)
    
    def test_signup_post_short_password(self):
        """너무 짧은 비밀번호로 회원가입 실패 테스트"""
        username = 'testuser3'
        data = self._create_signup_data(
            username=username,
            password1='123',
            password2='123'
        )
        
        response = self.client.post(self.signup_url, data)
        self._assert_signup_failed(response, username)
    
    def test_signup_post_duplicate_username(self):
        """중복된 사용자명으로 회원가입 실패 테스트"""
        username = 'existinguser'
        User.objects.create_user(username=username, password='pass123')
        
        data = self._create_signup_data(username=username)
        response = self.client.post(self.signup_url, data)
        
        self._assert_signup_failed(response, username)
        # 유저가 하나만 있는지 확인 (새로 생성 안됨)
        self.assertEqual(User.objects.filter(username=username).count(), 1)

    def test_signup_post_duplicate_username(self):
        """중복된 사용자명으로 회원가입 실패 테스트"""
        username = 'existinguser'
        User.objects.create_user(username=username, password='pass123')
        
        data = self._create_signup_data(username=username)
        response = self.client.post(self.signup_url, data)
        
        # 중복 케이스는 헬퍼 사용 안 함 (유저가 이미 존재하므로)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertTrue(response.context['form'].errors)
        # 유저가 하나만 있는지 확인 (새로 생성 안됨)
        self.assertEqual(User.objects.filter(username=username).count(), 1)

class PracticeViewsTest(TestCase):
    """연습용 뷰 기본 동작 확인"""
    
    def setUp(self):
        # 테스트용 Question 데이터 생성
        self.q1 = Question.objects.create(
            question_text="SQL 배우기",
            pub_date=timezone.now() - datetime.timedelta(days=1)
        )
        self.q2 = Question.objects.create(
            question_text="Django 배우기",
            pub_date=timezone.now() + datetime.timedelta(days=1)
        )
    
    def _get_json(self, url, params=None):
        """JSON API 요청 헬퍼"""
        query_string = f"?{params}" if params else ""
        response = self.client.get(f"{url}{query_string}")
        self.assertEqual(response.status_code, 200)
        return response.json()
    
    def _assert_html_contains(self, url, params, *expected_texts):
        """HTML 응답에 특정 텍스트 포함 확인 헬퍼"""
        query_string = f"?{params}" if params else ""
        response = self.client.get(f"{url}{query_string}")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        for text in expected_texts:
            self.assertIn(text, content)
    
    # Practice 1: 쿼리스트링 기본
    def test_practice_1_with_query(self):
        self._assert_html_contains('/polls/practice-1/', 'q=hello', 'hello')
    
    def test_practice_api_1_json(self):
        data = self._get_json('/polls/practice-api-1/', 'q=test')
        self.assertEqual(data['q'], 'test')
    
    # Practice 2: 검색 필터
    def test_practice_2_with_search(self):
        self._assert_html_contains('/polls/practice-2/', 'q=SQL', 'SQL', '결과 개수: 1')
    
    def test_practice_2_without_search(self):
        self._assert_html_contains('/polls/practice-2/', '', '결과 개수: 2')
    
    def test_practice_api_2_search(self):
        data = self._get_json('/polls/practice-api-2/', 'q=Django')
        self.assertEqual(data['q'], 'Django')
        self.assertEqual(data['count'], 1)
        self.assertIn('results', data)
    
    # Practice 3: 미래 질문
    def test_practice_3_hide_future(self):
        self._assert_html_contains('/polls/practice-3/', '', '결과:1')
    
    def test_practice_3_show_future(self):
        self._assert_html_contains('/polls/practice-3/', 'show=future', '결과:2')
    
    def test_practice_api_3_future(self):
        data = self._get_json('/polls/practice-api-3/', 'show=future')
        self.assertEqual(data['show'], 'future')
        self.assertEqual(data['count'], 2)
    
    # Practice 5: 날짜 필터
    def test_practice_5_with_dates(self):
        start = (timezone.now() - datetime.timedelta(days=2)).date().isoformat()
        end = timezone.now().date().isoformat()
        self._assert_html_contains('/polls/practice-5/', f'start={start}&end={end}', '결과:1')
    
    def test_practice_api_5_dates(self):
        data = self._get_json('/polls/practice-api-5/', 'start=2026-01-01')
        self.assertEqual(data['start_raw'], '2026-01-01')
        self.assertIsNotNone(data['start'])
    
    def test_practice_api_5_invalid_date(self):
        """잘못된 날짜로 parse_yyyy_mm_dd except 커버"""
        data = self._get_json('/polls/practice-api-5/', 'start=invalid&end=wrong')
        self.assertIsNone(data['start'])
        self.assertIsNone(data['end'])
    
    # Practice 6: 정렬
    def test_practice_6_oldest(self):
        self._assert_html_contains('/polls/practice-6/', 'order=oldest', 'order=oldest')
    
    def test_practice_6_latest(self):
        self._assert_html_contains('/polls/practice-6/', '', 'order=None')
    
    def test_practice_api_6_oldest(self):
        data = self._get_json('/polls/practice-api-6/', 'order=oldest')
        self.assertEqual(data['order'], 'oldest')
    
    # Practice Index
    def test_practice_index_page(self):
        response = self.client.get('/polls/practice/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/practice_index.html')
        self.assertIn('url_list', response.context)



# 기존코드
# # 모델 메서드 테스트(변경됨)
# class QuestionModelTests(TestCase):
#     def setUp(self):
#         """
#         매 테스트마다 사용할 기본 질문 객체 3종 생성
#         """
#         now = timezone.now()
#         self.future_question = Question(pub_date=now + datetime.timedelta(days=30))
#         self.old_question = Question(pub_date=now - datetime.timedelta(days=1, seconds=1))
#         self.recent_question = Question(pub_date=now - datetime.timedelta(hours=23, minutes=59, seconds=59))

#     def test_was_published_recently_with_future_question(self):
#         """미래 질문은 최근 게시된 것이 아니므로 False"""
#         self.assertIs
#         (self.future_question.was_published_recently(), False)

#     def test_was_published_recently_with_old_question(self):
#         """1일 이상 지난 과거 질문은 False"""
#         self.assertIs
#         (self.old_question.was_published_recently(), False)

#     def test_was_published_recently_with_recent_question(self):
#         """24시간 이내의 질문은 True"""
#         self.assertIs
#         (self.recent_question.was_published_recently(), True)

# # Index 뷰 테스트(변경없음)
# class QuestionIndexViewTests(TestCase):
#     def setUp(self):
#         self.url = reverse("polls:index")

#     def test_no_questions(self):
#         """질문이 없을 경우 메시지 출력"""
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerySetEqual
#         (response.context["latest_question_list"], [])

#     def test_past_question(self):
#         """과거 질문은 목록에 보여야 함"""
#         question = create_question("Past question", days=-30)
#         response = self.client.get(self.url)
#         self.assertQuerySetEqual
#         (response.context["latest_question_list"], [question])

#     def test_future_question(self):
#         """미래 질문은 목록에 보이면 안 됨"""
#         create_question("Future question", days=30)
#         response = self.client.get(self.url)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerySetEqual
#         (response.context["latest_question_list"], [])

#     def test_future_question_and_past_question(self):
#         """과거 질문만 목록에 표시되어야 함"""
#         past_question = create_question("Past question", days=-30)
#         create_question("Future question", days=30)
#         response = self.client.get(self.url)
#         self.assertQuerySetEqual
#         (response.context["latest_question_list"], 
#         [past_question])

#     def test_two_past_questions(self):
#         """과거 질문이 여러 개일 경우 최신 순으로 정렬되어야 함"""
#         q1 = create_question("Past question 1", days=-30)
#         q2 = create_question("Past question 2", days=-5)
#         response = self.client.get(self.url)
#         self.assertQuerySetEqual
#         (response.context["latest_question_list"], [q2, q1])

# # Detail 뷰 테스트(변경없음)
# class QuestionDetailViewTests(TestCase):
#     def test_future_question(self):
#         """미래 질문 상세 페이지는 404 반환"""
#         future_question = create_question(
#             "Future question", 
#             days=5
#             )
#         url = reverse("polls:detail", args=(future_question.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)

#     def test_past_question(self):
#         """과거 질문 상세 페이지는 접근 가능"""
#         past_question = create_question("Past question", days=-5)
#         url = reverse("polls:detail", args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_question.question_text)