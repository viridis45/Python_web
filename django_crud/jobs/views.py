# jobs > views.py
from django.shortcuts import render
import requests
from .models import Job
from faker import Faker

# Create your views here.
def index(request):
    return render (request, 'jobs/index.html')

def past_life(request):
    name = request.POST.get('name')
    listednames = Job.objects.all().values('name')
    fake = Faker()#'ko_KR')

    if name in listednames:
        past_job = request.POST.get('past_job')
        context = {
            'name': name,
            'past_job' : past_job,
            }

    else:
        past_job = fake.job()
        context = {
            'name' : name,
            'past_job' : past_job,
            }
        Job(name=name, past_job=past_job).save()

    from decouple import config
    GIPHY_API_KEY = config('GIPHY_API_KEY')
    url = f'http://api.giphy.com/v1/gpipifs/search?api_key={GIPHY_API_KEY}&q={past_job}'
    data = requests.get(url).json()
    #print(url)
#    image = data['images'][0]['original']['url']
    image = data.get('data')[0].get('images').get('original').get('url')
    print (image)
    context['image'] = image


    # db 에 이름이 있는지 확인. 같은 이름이 있을 시 기존 이름의 past_job 가져오기
    # 없으면 db에 저장한 수 가져오기
    #name = request.POST.get('name')
    #person = Job.objects.filter(name=name).first()
    #if person:
    #   past_job = person.past_job
    #else:
    #   person = Job(name=name, past_job=past_job)
    #   person.save()

    return render(request, 'jobs/past_life.html', context)




