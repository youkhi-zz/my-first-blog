from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Post, Question, Choice
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect
from django.http import Http404
from django.urls import reverse
from django.views import generic

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
    return render(request, 'myblog/post_main.html',context)

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

class IndexView(generic.ListView):
    template_name = 'myblog/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'myblog/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'myblog/results.html'

def throw(request):
    return render(request, 'throw.html')

def catch(request):
    message = request.GET.get('message')
    return render(request, 'catch.html', {'message':message})

def naver(request):
    return render(request, 'naver.html')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myblog/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myblog/results.html', {'question': question})