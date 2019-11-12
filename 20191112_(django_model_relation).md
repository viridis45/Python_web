## Adding Gravatar

1. pip install django-extensions

2. add on settings django_extensions (underscore)

3. python manage.py shell_plus

   1. import hashlib
   2. hashlib.md5('emailaddress').hexdigest()
      1. returns unicode error
   3. hashlib.md5('emailaddress'.encode('utf-8')).hexdigest()
      1. returns hashcode
   4. https://www.gravatar.com/avatar/theLongHashYouGotFromIt
   5. exit

4. Creat CustumUserCreateForm on articles>forms.py

   ```
   class CustomUserCreationForm(UserCreationForm):
       class Meta(UserCreationForm.Meta):
           # username, password1, password2, email
           fields = UserCreationForm.Meta.fields + ('email',)
   ```

   1. change def signup

5. < img src="https://www.gravatar.com/avatar/{{ gravater_url }}?d=mp" alt="gravatar_url" >

   1. 이런식으로 메일계정의 사진 가져오기
   2. ?d=mp는 디폴트그림

6. 







# anotherone_ORM

1. django-admin startproject modelrelation .

2. set up database and start shell_plus

3. ```
   In [4]: for article in user1.article_set.all():
      ...:     for comment in article.comment_set.all():
      ...:         print(comment.content)
   ```

4. article.user

5. article.like_users

6. user.article_set : 유저가 작성한 게시글들

7. c2.user_id (faster than below)

8. c2_user.pk (query the db once more so slower than the above)

9. article1.comment_set.all()[0].user.name

10. user2.comment_set.order_by('-content')

11. In [22]: comment = Comment.objects.values('user').get(pk=1)

    In [23]: comment
    Out[23]: {'user': 1}

    In [24]: user2.comments.set_all()

12. Article.objects.filter(title='1글')

13. 

## M:N 연결

1. 두 테이블을 m:n연결 시에는 중간에 중계 테이블을 생성함

   ```python
   # models.py
   
   class Reservation(models.Model):
        doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
        patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
   
        def __str__(self):
            return f'{self.doctor} 사의 {self.patient}환자'
   ```

2. 혹은

   ```python
   # models.py
   from django.db import models
   
   class Doctor(models.Model):
       name = models.TextField()
   
       def __str__(self):
           return f'{self.pk} 번 의사 {self.name}'
   
   
   class Patient(models.Model):
       name = models.TextField()
       doctors = models.ManyToManyField(Doctorm related_name='patients')
   
       def __str__(self):
           return f'{self.pk} 번 환자 {self.name}'
   
   ```

   

# Like 기능

## going back to FORM 프로젝트

1. user.article_set

2. Article class에 

   ```python
       like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, 
                                       related_name='like_articles',
                                       blank = True)
   ```

3. ```python
   # views.py 에 추가
   
   def like(request, article_pk):
       article = get_object_or_404(Article, pk=article_pk)
       user = request.user
   
       # 해당 게시글에 좋아요를 누른 사람들 중에 
       # user.pk를 가진 유저가 존재하면
       if article.like_users.filter(pk=user.pk).exists():
           # 유저를 삭제하고 좋아요를 취소
           article.like_users.remove(user)
       else:
           article.like_users.add(user)
       return redirect('articles:index')
   ```

4. 