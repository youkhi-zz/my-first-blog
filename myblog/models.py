from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    password = models.CharField(max_length=32, default='1234')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def delete(self):
        self.delete()

    # GUI가 없는 환경에서 유용
    # text도 출력할 수 있도록
    def __str__(self):
        return self.title

'''
class Translator(models.Model):
    input=models.CharField(max_length=50)
    output=models.CharField(max_length=50)
'''
