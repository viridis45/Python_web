from django import forms
from .models import Article, Comment

#class ArticleForm(forms.Form):
    # max length 가 있는 반면, min lenght도 있음 optional.
#    title = forms.CharField(
#        max_length = 10,
#        label = 'title',
#        widget=forms.TextInput(
#            attrs={'class':'mytitle', 'placeholder':'enter the title'}
#        ))

 #   content = forms.CharField(
 #       min_length = 5, 
 #       widget=forms.Textarea(
 #           attrs={'class':'mycontent',
 #           'placeholder':'Enter the content',
 #           'rows':5,
 #           'cols':50}
 #       ))
    
class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        max_length = 10,
        widget = forms.TextInput(attrs = {
            'class' : 'title',
            'placeholder' : 'Enter the title',
        })
    ) # 없어도 되는게 커스터마이징으로 추가. 메타부분만 필요.


    class Meta:
        model = Article
        #fields = "__all__"
        fields = ('title', 'content')
# Article class의 모든것을 따로 지정하지 않아도 가져올 수 있음



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )