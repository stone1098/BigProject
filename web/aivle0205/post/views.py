from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(req):
    page = req.GET.get('page', '1')
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    today = datetime.today().date()
    context = {'question_list': page_obj, 'today': today}
    return render(req, 'post/question_list.html', context)

def detail(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    today = datetime.today().date()
    context = {'question': question, 'today': today}
    return render(req, 'post/question_detail.html', context)

@login_required(login_url='accounts:login')
def question_create(req):
    if req.method == 'POST':
        form = QuestionForm(req.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if req.FILES:
                question.image = req.FILES['image']
            question.user = req.user
            question.save()
            return redirect('post:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(req, 'post/question_form.html', context)

@login_required(login_url='accounts:login')
def question_modify(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if req.user != question.user:
        messages.error(req, '수정권한이 없습니다')
        return redirect('post:detail', question_id=question.id)
    
    if req.method == 'POST':
        form = QuestionForm(req.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            if req.FILES:
                question.image = req.FILES['image']
            question.save()
            return redirect('post:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'question': question,}
    return render(req, 'post/question_form.html', context)

@login_required(login_url='accounts:login')
def question_delete(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if req.user != question.user:
        messages.error(req, '삭제권한이 없습니다')
        return redirect('post:detail', question_id=question.id)
    question.delete()
    return redirect('post:index')

@login_required(login_url='accounts:login')
def answer_create(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = Answer(question=question,
                    content=req.POST.get('content'), user=req.user)
    answer.save()
    return redirect('post:detail', question_id=question.id)

# @login_required(login_url='common:login')
# def answer_modify(req, answer_id):
#     answer = get_object_or_404(Answer, pk=answer_id)
#     # if req.user != answer.user:
#     #     messages.error(req, '수정권한이 없습니다')
#     #     return redirect('pybo:detail', question_id=answer.question.id)
#     if req.method == "POST":
#         form = AnswerForm(req.POST, instance=answer)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.modify_date = timezone.now()
#             answer.save()
#             return redirect('post:detail', question_id=answer.question.id)
#     else:
#         form = AnswerForm(instance=answer)
#     context = {'answer': answer, 'form': form}
#     return render(req, 'post/answer_form.html', context)

@login_required(login_url='accounts:login')
def answer_delete(req, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if req.user != answer.user:
        messages.error(req, '삭제권한이 없습니다')
        return redirect('post:detail', question_id=answer.question.id)
    answer.delete()
    return redirect('post:detail', question_id=answer.question.id)

# @login_required(login_url='accounts:login')
# def reply_create(req, answer_id):
#     answer = get_object_or_404(Answer, pk=answer_id)
#     question = get_object_or_404(Question, pk=answer.question.id)