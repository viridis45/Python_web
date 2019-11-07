from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.views.decorators.http import require_POST
from IPython import embed

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {'articles' : articles}

    return render(request, 'articles/index.html', context)


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
 
            article = form.save()
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


    comment_form = CommentForm()
    context = {'article':article, 'comment_form':comment_form, 'comments':comments}
    return render(request, 'articles/detail.html', context)
    



@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.delete()
    return redirect('articles:index')

# require_post를 더하면서 아래에서 업데이트
#    if request.method == 'POST':
#        article.delete()
#        return redirect('articles:index')
#    else:
#        return redirect('articles:detail', article_pk)


def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method =='POST':
#        form = ArticleForm(request.POST) 11.07 수정
        form = ArticleForm(request.POST, instance=article)    
        if form.is_valid():
            form.save()
#            article.title = form.cleaned_data.get('title') 11.07 수정. form.save()로 대체가능
#            article.content = form.cleaned_data.get('content')
#            article.save()
            return redirect('articles:detail', article_pk)
    else:
        form = ArticleForm(
            # initial={'title' : article.title, 
            # 'content': article.content} 11.07 추가 후 instance=article 첨가하며 수정
            instance = article
            )
    context = {'form' : form }
    return render(request, 'articles/create.html', context)


@require_POST
def comments_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm(require.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.save()
#    if request.method == 'POST':
#        comment_form = CommentForm(request.POST)
#        if comment_form.is_valid():
#            comment = comment_form.save(commit=False)
#            comment.article = article
#            comment.save()
    return redirect('articles:detail', article_pk)



@require_POST
def comments_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk = comment_pk)
    comment.delete()

#    if request.method == 'POST':
#        comment = get_object_or_404(Comment, pk = comment_pk)
#        comment.delete()
    return redirect("articles:detail", article_pk)