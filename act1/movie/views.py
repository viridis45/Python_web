# act1 > movie > views.py

from django.shortcuts import render, redirect
from .models import Movies
from decouple import config
import requests


def index(request):
    #movies = Movies.objects.values_list('pk', 'title', 'score')
    # 로 했더니 튜플을 주더라
    movies = Movies.objects.values('pk', 'title', 'score')
    context = {
        'movies' : movies
    }
    return render(request, 'movie/index.html', context)

def info(request, pk):
    movie = Movies.objects.get(pk=pk)
    context = {
        'movie' : movie
    }


    GIPHY_API_KEY = config('GIPHY_API_KEY')
    url = f'http://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={movie.title}'
    data = requests.get(url).json()
    image = data.get('data')[0].get('images').get('original').get('url')
    context['image'] = image

    return render(request, 'movie/info.html', context)

def new(request):
    if request.method == 'POST':
#        log = dict(request.POST)
#        del log['csrfmiddlewaretoken']
#        newlog = Movies(**log)
#        newlog.save() # Shawn said don't do dis

        title = request.POST.get('title') # but i hate my life now
        audience = request.POST.get('audience')
        open_date = request.POST.get('open_date')
        genre = request.POST.get('genre')
        score = request.POST.get('score')

        Movies.objects.create(title=title, audience=audience, open_date=open_date,
        genre=genre, score=score).save()

        return redirect('movie:index')
    else:
        return render(request, 'movie/new.html')

def edit(request, pk):
    if request.method == 'POST':
        movie = Movies.objects.get(pk=pk)

        movie.title = request.POST.get('title')
        movie.audience = request.POST.get('audience')
        movie.open_date = request.POST.get('open_date')
        movie.genre = request.POST.get('genre')
        movie.score = request.POST.get('score')

        movie.save()
        return redirect('movie:info', movie.pk)

    else:
        movie = Movies.objects.get(pk=pk)
        context = { 'movie' : movie }
        return render(request, 'movie/edit.html', context)

def delete(request, pk):
    movie = Movies.objects.get(pk=pk)
    movie.delete()
    return redirect('movie:index')

