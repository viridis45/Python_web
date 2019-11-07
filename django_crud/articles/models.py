from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('articles:detail', args=[str(self.pk)])


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments') #cascade == 게시글이 삭제되는 경우 댓글들도 삭제되도록 한다
    # realted name을 더함으로써 기존 : article.comment_set.all() 에서 article.comments.all()로 가져오기


    class Meta :
        ordering = ['-pk', ]# 가장 최신에 작성된걸 맨 위로 출력되게 한다.


    def __str__(self):
        return f'<Article({self.article_id}): Comment({self.pk})-{self.content}>'




