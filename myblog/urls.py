from django.urls import path 
from . import views

# 두 번째 인자에서 view.py로 연결할 수 있도록 해야 함
# 그러기 위해서 views를 import해 온 것
urlpatterns = [
    path('', views.travel, name='travel'), # home
    path('guestbook/', views.post_main, name='post_main'),    # guestbook
    path('translator/', views.translator, name='translator'),
    path('about/', views.about, name='about'),  # about  
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit')
]