from django.shortcuts import render
import random
import requests

# Create your views here.
def index(request):
    return render(request, 'pages/index.html')

# throw & catch 연습
def throw(request):
    return render(request, 'pages/throw.html')

def catch(request):

    print(request)
    print(request.scheme)
    print(request.path)
    print(request.method)
    print(request.headers)
    print(request.META)
    print(request.GET)

    message = request.GET.get("message")
    message2 = request.GET.get("message2")
    context = {
        'message': message,
        'message2': message2,
    }
    return render(request, 'pages/catch.html', context)

# 로또 번호 추첨
def lotto_pick(request):
    return render(request, 'pages/lotto_pick.html')

def lotto_get(request):
    lottos = range(1, 46)
    pick = random.sample(lottos, 6)
    name = request.GET.get("name")

    context = {
        'name': name,
        'pick': pick
    }
    return render(request, 'pages/lotto_get.html', context)

# 실제 로또 번호로 당첨 확인하기
def lottery(request):
    return render(request, 'pages/lottery.html')

def jackpot(request):
    
    # 1. 사용자의 이름을 받아오자.
    name = request.GET.get("name")
    
    # 2. 나눔로또 API로 요청을 보내 결과 받기
    res = requests.get("https://dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=882")
    res = res.json()

    # 3. 로또 당첨번호 6개를 골라 winner 리스트에 담자!
    winner = []
    for i in range(1, 7):
        winner.append(res[f'drwtNo{i}'])

    # 4. 1~45 까지의 수 중에서 6개를 뽑아 리스트에 담자
    picked = random.sample(range(1, 46), 6)

    # 5. set를 활용해 교집합 연산을 활용, 실제 로또 당첨 번호와 컴시기가 뽑아준 번호의 개수 구하기
    matched = len(set(winner) & set(picked))

    # 6. 매칭 결과에 따라 다른 응답 메세지 나타내기 (보너스 번호 제외)
    if matched == 6:
        result = '1등입니다, 퇴사!'
    elif matched == 5:
        result = '3등입니다. 퇴사는 위험. 휴가 고고'
    elif matched == 4:
        result = '4등입니다. 그냥 술이나 한잔...'
    elif matched == 3:
        reuslt = "5등입니다. 다시 로또나 삽시당..."
    else:
        result = '꽝... '

    # 7. 딕셔너리를 넘기자!
    context = {
        'name': name,
        'result': result,
    }
    return render(request, 'pages/jackpot.html', context)

def user_new(request):
    return render(request, 'pages/user_new.html')

def user_create(request):
    name = request.POST.get("name")
    password = request.POST.get("password")
    # name = request.GET.get("name")
    # password = request.GET.get("password")
    context = {
        'name': name,
        'password': password
    }
    return render(request, 'pages/user_create.html', context)

def static_example(request):
    return render(request, 'pages/static_example.html')

def art(request):
    return render(request, 'pages/art.html')

def result(request):
    # 1. form 태그로 날린 데이터를 받는다. (GET방식)
    word = request.GET.get("word")

    # 2. ARTII api로 요청을 보낸다.
    artii = requests.get(f'http://artii.herokuapp.com/make?text={word}').text
    context = {
        'artii': artii
    }
    return render(request, 'pages/result.html', context)