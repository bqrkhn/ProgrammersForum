from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, get_object_or_404
from .form import QuestionForm, AnswerForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import Question, Answer, Vote, User
from django.db.models import Q
from main.models import Profile, Activity
from difflib import SequenceMatcher
from main.form import Loginform


# Create your views here.

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def ask(request):
    return render(request, 'discussions/ask.html', {"form": QuestionForm()})


@login_required
def index(request):
    if request.method == "POST" and request.POST.get('title', None) and request.POST.get('description', None):
        question = Question.objects.create(title=request.POST["title"], description=request.POST["description"],
                                           username=User.objects.get(username=request.user.username))
        question.save()
        Activity.objects.create(by_username=User.objects.get(username=request.user.username), QID=question,
                                type=True).save()
        return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': "Q" + str(question.id)}))
    return render(request, 'discussions/discussion.html',
                  {"questions": Question.objects.all(), "activities": Activity.objects.all()[:10]})


@login_required
def question(request, question_id):
    question_id = int(question_id[1:])
    question = get_object_or_404(Question, id=question_id)
    questions = Question.objects.all()
    related = []
    answers = Answer.objects.filter(QID=question)
    for q in questions:
        score = (similar(q.title, question.title))
        if score > 0.3 and score != 1:
            related.append(q)
    votes = Vote.objects.filter(username=User.objects.get(username=request.user.username)).filter(
        Q(QID=question_id) | Q(AID__in=Answer.objects.filter(QID=question_id).values_list('id', flat=True)))
    return render(request, 'discussions/question.html',
                  {"question": question, "votes": votes, "related": related, "answers": answers,
                   "activities": Activity.objects.all()[:7], "form": AnswerForm()})


@login_required
def answer(request, question_id):
    question_id = int(question_id[1:])
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST" and request.POST.get('description', None):
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(username=user)
        answer = Answer.objects.create(QID=question,
                                       description=request.POST['description'],
                                       username=user)
        profile.points += 2
        profile.save()
        answer.save()
        question.count += 1
        question.save()
        Activity.objects.create(by_username=User.objects.get(username=request.user.username), type=True, QID=question,
                                AID=answer).save()
    return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': "Q" + str(question.id)}))


def vote(request):
    id = request.GET.get('id', None)
    type = request.GET.get('type', None)
    if id[0] == 'Q':
        id = id[1:]
        question = Question.objects.get(id=id)
        user = Profile.objects.get(username=User.objects.get(username=question.username))
        if int(type) == 1:
            question.votes += 1
            user.points += 1
            vote = Vote.objects.filter(username=User.objects.get(username=request.user.username), QID=question,
                                       vote=False)
            Activity.objects.create(by_username=User.objects.get(username=request.user.username), QID=question,
                                    on_username=User.objects.get(username=question.username), vote=True).save()
            if vote.exists():
                vote.delete()
            else:
                Vote.objects.create(username=User.objects.get(username=request.user.username), QID=question, vote=True)
        else:
            question.votes -= 1
            user.points -= 1
            vote = Vote.objects.filter(username=User.objects.get(username=request.user.username), QID=question,
                                       vote=True)
            Activity.objects.create(by_username=User.objects.get(username=request.user.username), QID=question,
                                    on_username=User.objects.get(username=question.username), vote=False).save()
            if vote.exists():
                vote.delete()
            else:
                Vote.objects.create(username=User.objects.get(username=request.user.username), QID=question, vote=False)
        user.save()
        question.save()
    else:
        id = id[1:]
        print(id)
        answer = Answer.objects.get(id=id)
        user = Profile.objects.get(username=User.objects.get(username=answer.username))
        if int(type) == 1:
            answer.votes += 1
            user.points += 1
            vote = Vote.objects.filter(username=User.objects.get(username=request.user.username), AID=answer,
                                       vote=False)
            Activity.objects.create(by_username=User.objects.get(username=request.user.username), AID=answer,
                                    QID=Question.objects.get(id=answer.QID.id),
                                    on_username=User.objects.get(username=answer.username), vote=True).save()
            if vote.exists():
                vote.delete()
            else:
                Vote.objects.create(username=User.objects.get(username=request.user.username), AID=answer, vote=True)
        else:
            answer.votes -= 1
            user.points -= 1
            vote = Vote.objects.filter(username=User.objects.get(username=request.user.username), AID=answer, vote=True)
            Activity.objects.create(by_username=User.objects.get(username=request.user.username), AID=answer,
                                    QID=Question.objects.get(id=answer.QID.id),
                                    on_username=User.objects.get(username=answer.username), vote=False).save()
            if vote.exists():
                vote.delete()
            else:
                Vote.objects.create(username=User.objects.get(username=request.user.username), AID=answer, vote=False)
        answer.save()
        user.save()
    return JsonResponse({})


@login_required
def delete(request, id):
    if id[0] == 'Q':
        id = id[1:]
        question = get_object_or_404(Question, id=id)
        if question.username == request.user:
            return render(request, 'discussions/delete.html', {"question": question})
        else:
            return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': id}))
    else:
        id = id[1:]
        answer = get_object_or_404(Answer, id=id)
        if answer.username == request.user:
            return render(request, 'discussions/delete.html', {"answer": answer})
        else:
            return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': answer.QID.QID}))


@login_required
def confirm(request, id):
    if id[0] == 'Q':
        id = id[1:]
        question = get_object_or_404(Question, id=id)
        if question.username == request.user:
            question.delete()
            return HttpResponseRedirect(reverse('discussions:index'))
        else:
            return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': id}))
    else:
        id = id[1:]
        answer = get_object_or_404(Answer, id=id)
        if answer.username == request.user:
            temp_id = "Q" + str(answer.QID.id)
            answer.delete()
            return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': temp_id}))
        else:
            return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': answer.QID.id}))


@login_required
def edit(request, id):
    if request.method == "POST" and request.POST.get('description'):
        if id[0] == 'Q':
            id = id[1:]
            question = get_object_or_404(Question, id=id)
            question.title = request.POST.get('title')
            question.description = request.POST.get('description')
            question.save()
            return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': "Q" + str(id)}))
        else:
            id = id[1:]
            answer = get_object_or_404(Answer, id=id)
            answer.description = request.POST.get('description')
            answer.save()
            return HttpResponseRedirect(
                reverse('discussions:question', kwargs={'question_id': "Q" + str(answer.QID.id)}))
    else:
        if id[0] == 'Q':
            id = id[1:]
            question = get_object_or_404(Question, id=id)
            if question.username == request.user:
                return render(request, 'discussions/ask.html',
                              {"form": QuestionForm(instance=question), "question": question})
            else:
                return HttpResponseRedirect(reverse('discussions:question', kwargs={'question_id': "Q" + str(id)}))
        else:
            id = id[1:]
            answer = get_object_or_404(Answer, id=id)
            if answer.username == request.user:
                return render(request, 'discussions/ask.html',
                              {"form": QuestionForm(instance=answer), "answer": answer})
            else:
                return HttpResponseRedirect(
                    reverse('discussions:question', kwargs={'question_id': "Q" + str(answer.QID.id)}))
