from django.test import TestCase
from django.utils import timezone
import datetime
from django.urls import reverse 

from .models import Question
# Create your tests here.

class QuestioModelTest(TestCase):
    def test_was_published_recently_with_future_case(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publish_date = time)
        self.assertIs(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1 , seconds=1)
        # create a question with old time
        old_question = Question(publish_date = time)
        # check if it is published recently 
        self.assertIs(old_question.was_published_recently(),False)
    
    def test_was_published_within_a_day(self):
        # set a a time for a question
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        # create a question for above time
        recent_question = Question(publish_date = time)
        # check if is recently published or not?
        self.assertIs(recent_question.was_published_recently(),True)

def create_question(question_text,days):
    """
    create a question with question_text and publish_date offset by days

    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question = question_text,publish_date = time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """
        return 'no polls are availabe' when no questions exist
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'No polls are available')
        self.assertQuerySetEqual(response.context['question_list'],[])
        
    def test_past_question_should_appear(self):
        """
        question published in the past should be displayed at the index page
        """
        question = create_question("past question",days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['question_list'],[question])

    def test_future_questions_should_not_appear(self):
        """
        Questins published in future that should not displayed
        """
        question = create_question("future question",days=10)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response,'No polls are available')
        self.assertQuerySetEqual(response.context['question_list'],[question])
