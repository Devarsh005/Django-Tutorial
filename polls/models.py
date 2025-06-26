import datetime
from django.utils import timezone
from django.db import models
from django.contrib import admin

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=300)
    publish_date = models.DateTimeField('Date Published')

    def __str__(self):
        return self.question

    @admin.display(
        boolean=True,
        ordering="publish_date",
        description="Published recently?",)

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.publish_date <= timezone.now()

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete= models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # voter_name = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text