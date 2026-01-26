from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # 여기에 try-except 사용가능 할거같은데?
        # is_valid 가 유효성검사 이거 하나로 끝낸다.
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}님, 회원가입이 완료되었습니다!')
            return HttpResponseRedirect(reverse("login"))
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})