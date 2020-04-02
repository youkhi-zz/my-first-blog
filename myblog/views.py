from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
from .forms import PostForm, TranslatorForm
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .sampletranslator import sampletranslator


#from langdetect import detect_langs

# 함수의 인자로 request를 받음
# 템플릿 변수를 넘길 때 딕셔너리 형태로 넘겨야 함


def post_main(request): #guestbook
    if request.method == "POST": # if form is bind, 폼에 입력된 정보를 view로 가져올 때 
        form = PostForm(request.POST)
        if form.is_valid(): # 폼에 들어있는 값들이 올바른지
            post = form.save(commit=False)
            post.author = request.user # 수정 필요
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else: # form unbound, 사용자한테 렌더될 때 비어있거나 기본값을 가짐, 처음 화면을 열었을 때 비어있는 칸
        form = PostForm()

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    context = {'form':form, "posts":posts}
    return render(request, 'myblog/post_main.html', context)

# POST method needs to be used
# text to variable, variable to API, json to dynamic contents -> javascript
def translator(request):
    form=TranslatorForm()
    if request.method=="POST": # form에 입력된 정보를 view로 가져올 때
        form=TranslatorForm(request.POST)
        if form.is_valid():
            textvar=request.POST
            textvar=textvar['input']
            sampletranslator(textvar)
            # ? sampletranslator.py의 원래 파일 이름은 translator-text.py였음
            # ? 그런데 - 를 인식하지 못하는 듯 함
            # ? 이런 경우는 어떻게?
            # return redirect('translator')
    else:
        form=TranslatorForm() # 그냥 비어있는 화면

    context={'form':form}
    return render(request, 'myblog/translator.html', context)

def about(request):
    return render(request, 'myblog/about.html')

def travel(request):
    return render(request, 'myblog/travel.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'myblog/post_detail.html', {'post': post})

def post_auth(request,pk):
    post = get_object_or_404(Post, pk=pk) 

    if post.password is not None:
        # 구현필요  
        return render(request, 'myblog/post_auth.html', {'post':post})
 
    return redirect('post_edit', pk=post.pk)

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_main')

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'myblog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'myblog/post_edit.html', {'form': form})