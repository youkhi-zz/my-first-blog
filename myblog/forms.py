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

# https://stackoverflow.com/questions/17754295/can-i-have-a-django-form-without-model
class TranslatorForm(forms.Form):
     input = forms.CharField(help_text="<br/><br/>", required=True)
     output = forms.CharField(disabled=True, required=False)

# 폼은 브라우저랑 장고 api가 소통하도록 해주는 애, 그냥 텍스트 받아주는 애
