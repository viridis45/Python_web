from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from IPython import embed
import hashlib

# Create your views here.
def index(request):
    # if request.user.is_authenticated:
    #         gravatar_url = hashlib.md5(request.user.email.strip().lower().encode('utf-8')).hexdigest()
    # else:
    #     gravatar_url = None # making templatetags so deleting this part.
    articles = Article.objects.all()
    context = {'articles' : articles} #, 'gravatar_url':gravatar_url}
    return render(request, 'articles/index.html', context)

#@login_required(login_url='/accounts/test/')
@login_required
def create(request):
    #embed()
    if request.method == 'POST':
        
        # 폼 인스턴스를 생성하고 요청에 의한 데이터로 채운다 (binding)
        form = ArticleForm(request.POST)
        #embed()
        # 먼저 폼이 유효한지 체크한 뒤 데이터베이스에 저장함
        if form.is_valid():
#        11.05 맨 처음 방식
            # title = request.POST.get('title')
            # content = request.POST.get('content')
            # article = Article(title=title, content=content)
            # article.save() 
                
 #       11.06 form 적용한 뒤 의 방식
 #            title = form.cleaned_data.get('title')
 #           content = form.cleaned_data.get('content')
 #           article = Article(title=title, content=content)
 #           article.save() 
#       return redirect('articles:index')

 #      11.07 form의 형식을 바꾸고 나서 아래로 수정함
 
            article = form.save(commit=False)
            article.user=request.user
            article.save()
            
            # hashtaging
            for word in article.content.split():
                if word.startswith("#"):
                    hashtag, created = Hashtag.objects.get_or_create(content=word)
                    article.hashtags.add(hashtag)

            return redirect('articles:detail', article.pk)


    else:
        form = ArticleForm()
        context = {'form' : form}

    return render(request, 'articles/create.html', context)


def detail(request, article_pk):
    #article = Article.objects.get(pk=article_pk)
    article = get_object_or_404(Article, pk=article_pk)
    comments = Comment.objects.filter(article=article)

#    try:
#        article = Artivcle.objects.get(pk=article_pk)
#    except:
#        from django.http import Http404
#        raise Http404(' no article matches the given query')

    person = get_object_or_404(get_user_model(), pk = article.user_id)


    comment_form = CommentForm()
    context = {'article':article, 'comment_form':comment_form, 'comments':comments, 'person':person}
    return render(request, 'articles/detail.html', context)
    


# 로그인 후 원래 페이지로 돌아갈 떄 get방식으로 돌아가므로
# @login_required 사용 불가
@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated :
        article = get_object_or_404(Article, pk=article_pk)
        if request.user == article.user:
            article.delete()
        return redirect('articles:index')

    return HttpResponse("you are unauthorized", status=401)

# require_post를 더하면서 아래에서 업데이트
#    if request.method == 'POST':
#        article.delete()
#        return redirect('articles:index')
#    else:
#        return redirect('articles:detail', article_pk)


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.user == article.user: #11.11 수정, 작성자만 수정가능하게
        if request.method =='POST':
    #        form = ArticleForm(request.POST) 11.07 수정
            form = ArticleForm(request.POST, instance=article)    
            if form.is_valid():
                form.save()
    #            article.title = form.cleaned_data.get('title') 11.07 수정. form.save()로 대체가능
    #            article.content = form.cleaned_data.get('content')
    #            article.save()
                article.hashtags.clear()
                for word in article.content.split():
                    if word.startswith("#"):
                        hashtag, created = Hashtag.objects.get_or_create(content=word)
                        article.hashtags.add(hashtag)
                return redirect("articles:detail", article_pk)
        else:
            form = ArticleForm(
            # initial={'title' : article.title, 
            # 'content': article.content} 11.07 추가 후 instance=article 첨가하며 수정
            instance = article
            )
    else:
        return redirect('articles:index')
    context = {'form' : form }
    return render(request, 'articles/create.html', context)



@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated :
        article = get_object_or_404(Article, pk=article_pk)
        comment_form = CommentForm(require.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
    #    if request.method == 'POST':
#        comment_form = CommentForm(request.POST)
#        if comment_form.is_valid():
#            comment = comment_form.save(commit=False)
#            comment.article = article
#            comment.save()
        return redirect('articles:detail', article_pk)

    return HttpResponse('you are unauthorized', status=401)


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated :
        comment = get_object_or_404(Comment, pk = comment_pk)
        if request.user == comment.user:
            comment.delete()

#    if request.method == 'POST':
#        comment = get_object_or_404(Comment, pk = comment_pk)
#        comment.delete()
        return redirect("articles:detail", article_pk)
    return HttpResponse('you are unauthorized', status=401)


def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user # 요청을 보낸 유저
    
    # 해당 게시글에 좋아요를 누른 사람들 중에
    # user.pk를 가진 유저가 존재하면,
    if request.user.is_authenticated:
        if article.like_users.filter(pk=user.pk).exists():
            # user를 삭제하고 (좋아요를 취소)
            article.like_users.remove(user)
        else:
            article.like_users.add(user)
        return redirect("articles:index")
    return redirect("accounts:login")


@login_required
def follow(request, article_pk, user_pk):
    # 게시글 유저
    you = get_object_or_404(get_user_model(), pk=user_pk)
    # 현재 접속 유저
    me = request.user
    if you != me:
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect("articles:detail", article_pk)


def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    articles = hashtag.article_set.order_by("-pk")
    context = {'hashtag': hashtag, 'articles': articles}
    return render(request, 'articles/hashtag.html', context)