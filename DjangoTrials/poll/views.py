from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.template import loader


#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ' , '.join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('poll/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }
#    return HttpResponse(template.render(context, request))
    return render(request, 'poll/index.html', context)


def detail(request, question_id):
#    return HttpResponse("The current question is %s" % question_id)
    #try:
        #question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
        #raise Http404("Question not added")
    question = get_object_or_404(Question,pk = question_id)
    return render(request, 'poll/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})


def vote(request, question_id):
    #return HttpResponse("Your vote for question %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))
