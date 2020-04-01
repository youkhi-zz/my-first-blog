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

class UntranslatedForm(forms.ModelForm):
    class Meta:
        input = forms.CharField(help_text="Type what you want to translate!", required=True)

class TranslatedForm(forms.ModelForm):
    class Meta:
        output=forms.CharField(disabled=True)

# 폼은 브라우저랑 장고 api가 소통하도록 해주는 애, 그냥 텍스트 받아주는 애
