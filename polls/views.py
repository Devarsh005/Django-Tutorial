from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice
from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
# def index(request):
#     questions = Question.objects.order_by('publish_date')[:5]
#     output = [question.question for question in questions]
#     return HttpResponse(f"your desire output is {output}")

class IndexView(generic.ListView):
    """ represent main page where last 5 questions are showed
    """
    # ignore the commented code because commented code write without using generic views
    template_name = 'polls/index.html'
    # page = loader.get_template('polls/index.html')
    context_object_name = "question_list" # context_object_name assign the qurey_set return value 

    # list_of_questions = Question.objects.order_by('publish_date')[:5]
    # context = {"list_of_questions":list_of_questions}   # context must be dictionary rather than query set
    def get_queryset(self):
        """return the last 5 Question (not including those whose published date in future)"""
        
        return Question.objects.filter(publish_date__lte = timezone.now()).order_by('publish_date')[:5]
    # return HttpResponse(page.render(context,list_of_questions))

# def details(request,question_id):
#     """ show a particular question and choices based on particular question id
#     """
#     try:
#         question = Question.objects.get(id = question_id)
#         # choice = [c.choice_text for c in question.choice_set.all()]
#         context = {"question":question}
#     except Question.DoesNotExist:
#         raise Http404("question does not exist")
#     return render(request,"polls/details.html",context)

class DetailView(generic.DetailView):
    template_name = 'polls/details.html'
    model = Question

class Result(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'

# def result(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request , "polls/result.html",{"question":question})

def vote(request,question_id):
    """ save the votes and and count the votes of each question
    """
    question = get_object_or_404(Question,pk = question_id)
    try:
        voted_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request , 'polls/details.html', {
            'question' : question ,
            'error_message' : 'you did not select choice'
        })
        # return HttpResponse(f"yor are voting on {question_id}")
    else:
        voted_choice.votes = F('votes')+1
        voted_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question.id,)))