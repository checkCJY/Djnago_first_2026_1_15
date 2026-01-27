import datetime
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import generic
from django.shortcuts import render

from .models import Question 



def parse_yyyy_mm_dd(value: str):
    """
    'YYYY-MM-DD' → date로 변환
    실패하면 None
    """
    try:
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    

# 1️⃣ 연습 1: “쿼리스트링 값 꺼내기” (가장 기초)

# ✅ 목표
# - URL `?q=hello` 가 오면
# - `request.GET.get("q")`로 값을 꺼내서
# - 화면/JSON에 그대로 보여준다

def practice_1(request):
    q = request.GET.get("q")     # TODO : q 값을 꺼내기 
    return HttpResponse(f"q는 지금: {q}")

def practice_api_1(request):
    q = request.GET.get("q")        # TODO : q 값을 꺼내기
    return JsonResponse({"q": q})

# 2️⃣ 연습 2: 검색어가 있을 때만 필터하기

# ✅ 학생 목표
# - `q`가 있을 때만 `icontains` 필터 적용
# - `q`가 없으면 전체 목록 그대로
def practice_2(request):
    qs = Question.objects.all()
    q = request.GET.get("q")    # TODO : q 꺼내기

    # TODO : q가 있을 때만
    if q :  
        qs = qs.filter(question_text__icontains=q)

    # 결과 개수만 화면에 보여주기
    return HttpResponse(f"검색어: {q} / 결과 개수: {qs.count()}")

def practice_api_2(request):
    qs = Question.objects.all()
    q = request.GET.get("q") # TODO : q 꺼내기

    # TODO : q가 있을 때만
    if q :
        qs = qs.filter(question_text__icontains=q)

    return JsonResponse({
        "q": q,
        "count": qs.count(),
        "results": [{"id": x.id, "text": x.question_text} for x in qs[:10]]
    })

# 3️⃣ 연습 3 : “미래 질문 포함/숨기기 옵션”

# ✅ 목표
# - 기본: 미래 질문 제외
# - `show=future`일 때만 미래 질문 포함
def practice_3(request):
    qs = Question.objects.all()
    show = request.GET.get("show")  # TODO : show 값 꺼내기

    # future 가 대체 show의 어디에서 작동하는거지? 펍데이터?
    # 아마 장고 내부에서 처리하는 것 같은데, 알아봐야 겠다.
    # 그냥 ?show=future로 입력되면, 미래의 데이터가 보이고, 그 외의 값은 안보이는 방식
    if show != "future":  # TODO:  show가 future가 아니면
        qs = qs.filter(pub_date__lte=timezone.now())

    return HttpResponse(f"show={show} / 결과:{qs.count()}")

def practice_api_3(request):
    qs = Question.objects.all()
    show = show = request.GET.get("show")

    if show != "future":
        qs = qs.filter(pub_date__lte=timezone.now())

    return JsonResponse({
        "show": show,
        "count": qs.count(),
        "results": [{"id": x.id, "text": x.question_text} for x in qs[:10]]
    })


# 5️⃣ 연습문제 5 : “날짜 start / end 필터”

# ✅ 목표
# - `start=YYYY-MM-DD`가 오면 그 날짜 이후만
# - `end=YYYY-MM-DD`가 오면 그 날짜 이전만
# - 날짜 형식이 틀리면(None) 필터 적용 X


def practice_5(request):
    qs = Question.objects.all()

    # TODO : 시작과 끝값을 받아오자
    start_raw = request.GET.get("start")
    end_raw = request.GET.get("end")

    # 위에 공통함수에서 확인할 수 있다.
    # try 성공하면 date 객체가 오므로 if문 가능
    # except에 걸리면 none을 반환하므로 if문 작동안함
    start = parse_yyyy_mm_dd(start_raw)
    end = parse_yyyy_mm_dd(end_raw)

    if start:
        qs = qs.filter(pub_date__date__gte=start)

    if end:
        qs = qs.filter(pub_date__date__lte=end)

    return HttpResponse(f"start={start} end={end} / 결과:{qs.count()}")

def practice_api_5(request):
    qs = Question.objects.all()
    start_raw = request.GET.get("start")
    end_raw = request.GET.get("end")

    start = parse_yyyy_mm_dd(start_raw)
    end = parse_yyyy_mm_dd(end_raw)

    if start:
        qs = qs.filter(pub_date__date__gte=start)
    if end:
        qs = qs.filter(pub_date__date__lte=end)

    return JsonResponse({
        "start_raw": start_raw,
        "end_raw": end_raw,
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
        "count": qs.count(),
    })


# 6️⃣ 연습문제 6 : “정렬 order=oldest”

# ✅ 목표
# - 기본 최신순 `-pub_date`
# - `order=oldest`면 `pub_date` 오름차순

def practice_6(request):
    qs = Question.objects.all()
    order = request.GET.get("order")

    # order가 oldest 이면 오래된 것 부터 출력
    # 아니라면 최신순으로 출력
    if order == "oldest":
        qs = qs.order_by("pub_date")
    else:
        qs = qs.order_by("-pub_date")

    first = qs.first()
    return HttpResponse(f"order={order} / 첫 데이터: {first.pub_date if first else None}")

def practice_api_6(request):
    qs = Question.objects.all()
    order = request.GET.get("order")

    if order == "oldest":
        qs = qs.order_by("pub_date")
    else:
        qs = qs.order_by("-pub_date")

    return JsonResponse({
        "order": order,
        "first_pub_date": qs.first().pub_date.isoformat() if qs.exists() else None,
        "results": [{"id": x.id, "pub_date": x.pub_date.isoformat()} for x in qs[:5]]
    })


def practice_index(request):
    """쿼리스트링 연습 메뉴 페이지"""
    url_list = [
        {
            'category': '연습 1: 쿼리스트링 값 꺼내기 (기초)',
            'items': [
                {
                    'name': '기본 사용',
                    'url': '/polls/practice-1/?q=hello',
                    'description': 'q 파라미터로 "hello" 전달하기'
                },
                {
                    'name': '다른 값 테스트',
                    'url': '/polls/practice-1/?q=Django',
                    'description': 'q 파라미터로 "Django" 전달하기'
                },
                {
                    'name': 'API 버전 (JSON)',
                    'url': '/polls/practice-api-1/?q=test',
                    'description': 'JSON 형태로 응답 받기'
                },
            ]
        },
        {
            'category': '연습 2: 검색어 필터링',
            'items': [
                {
                    'name': '검색어 없이 (전체)',
                    'url': '/polls/practice-2/',
                    'description': 'q가 없으면 전체 Question 목록'
                },
                {
                    'name': '검색어로 필터',
                    'url': '/polls/practice-2/?q=SQL',
                    'description': '"SQL"이 포함된 질문만 검색'
                },
                {
                    'name': 'API 버전',
                    'url': '/polls/practice-api-2/?q=SQL',
                    'description': 'JSON으로 검색 결과 받기'
                },
            ]
        },
        {
            'category': '연습 3: 미래 질문 포함/제외',
            'items': [
                {
                    'name': '기본 (미래 질문 제외)',
                    'url': '/polls/practice-3/',
                    'description': 'show 파라미터 없으면 현재까지의 질문만'
                },
                {
                    'name': '미래 질문 포함',
                    'url': '/polls/practice-3/?show=future',
                    'description': 'show=future로 미래 질문까지 포함'
                },
                {
                    'name': 'API 버전 (미래 포함)',
                    'url': '/polls/practice-api-3/?show=future',
                    'description': 'JSON으로 미래 질문까지 받기'
                },
                
            ]
        },
        {
            'category': '연습 5: 날짜 start / end 필터',
            'items': [
                {
                    'name': '기본 (미래 질문 제외)',
                    'url': '/polls/practice-5/',
                    'description': 'show 파라미터 없으면 현재까지의 질문만'
                },
                {
                    'name': '미래 질문 포함',
                    'url': '/polls/practice-5/?start=2026-01-01',
                    'description': 'show=future로 미래 질문까지 포함'
                },
                {
                    'name': 'API 버전 31일 까지',
                    'url': '/polls/practice-api-5/?end=2026-01-31',
                    'description': 'JSON으로 1월 31일까지 기록 받기'
                },
                
            ]
        },
        {
            'category': '연습 6: 정렬 order=oldest',
            'items': [
                {
                    'name': '기본, order=oldest인 경우',
                    'url': '/polls/practice-6/?order=oldest',
                    'description': 'order가 oldest인 경우엔?'
                },
                {
                    'name': '그렇다면, order!=oldest는?',
                    'url': '/polls/practice-6/?order=latst',
                    'description': '나는 최신글을 보고싶은걸?'
                },
                {
                    'name': 'API 버전 확인해보자',
                    'url': '/polls/practice-api-6/?order=자유롭게작성',
                    'description': 'order를 자유롭게 작성해보세요'
                },
                
            ]
        },
    ]
    
    return render(request, 'polls/practice_index.html', {'url_list': url_list})