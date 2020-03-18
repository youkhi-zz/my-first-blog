from django import forms
from .models import Post

# model 클래스로부터 폼을 자동 생성

class PostForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput, required=True)
        model = Post
        author = forms.CharField()
        #fileds는 model의 일부만 사용하고자 할 때
        fields = ('title', 'author', 'text', 'password')
