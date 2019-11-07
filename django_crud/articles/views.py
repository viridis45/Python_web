from django.shortcuts import render, redirect
from .models import Article, Comment

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

def new(request):
    return render(request, 'articles/new.html')

def create(request):
    title = request.POST.get("title")
    content = request.POST.get("content")
    Article.objects.create(title=title, content=content).save()
    #return render(request, 'articles/index.html') # render는 context의 내용을 가지고 설계
    return redirect('articles:index')

def detail(request, pk):
    article=Article.objects.get(pk=pk)
    #comments = Comment.objects.filter(pk=article.pk)
    comments = article.comments.all()
    context={'article': article, 'comments':comments}
    return render(request, 'articles/details.html', context)

def delete(request, pk):
    article=Article.objects.get(pk=pk)
    article.delete()
    # return redirect('/articles/')
    return redirect('articles:index')

def edit(request, pk):
    article=Article.objects.get(pk= pk)
    context= {'article':article}
    return render(request, 'articles/edit.html', context)

def update(request,pk):
    article = Article.objects.get(pk=pk)
    content= request.POST.get('content')
    title = request.POST.get('title')
    article.title = title
    article.content = content
    article.save()
    return redirect('/articles/')




# added on 2019.10.31
def comments_create(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST': # 커멘트 저장
        # form 에서 넘어온 댓글 정보
        newcomment = request.POST.get('newcomment')
        Comment.objects.create(content = newcomment, article = article).save() #article = 에서 pk로 연결이 아닌 article자체로 넘겨주기
        return redirect('articles:detail', article.pk)

        # 댓글 생성 및 저장 후 리턴

        
    else:
        pass
    
    return redirect(article) #get_absolute_url통함
 


def comments_delete(request, article_pk, comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
        return redirect('articles:detail', article_pk)

    else:
        return redirect('article:detail', article_pk)
