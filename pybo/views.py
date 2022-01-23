from curses.ascii import HT
import imp
from multiprocessing import context
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import AnswerForm, QuestionForm
from django.core.paginator import Paginator

MAX_LIST_CNT = 10
MAX_PAGE_CNT = 5

# Create your views here.


def index(request):
    """
    pybo 목록 출력
    """
    # page 번호
    page = request.GET.get("page", "1")
    # 질문 리스트
    question_list = Question.objects.order_by("-create_date")
    # 페이징 처리, 페이징 처리할 리스트와 페이지당 수
    paginator = Paginator(question_list, MAX_LIST_CNT)

    last_page_num = 0
    for last_page in paginator.page_range:
        last_page_num = last_page_num + 1

    current_block = ((int(page) - 1) / MAX_PAGE_CNT) + 1
    current_block = int(current_block)

    page_start_number = ((current_block - 1) * MAX_PAGE_CNT) + 1

    page_end_number = page_start_number + MAX_PAGE_CNT - 1

    page_obj = paginator.get_page(page)
    context = {
        "question_list": page_obj,
        "list_page_num": last_page_num,
        "page_start_number": page_start_number,
        "page_end_number": page_end_number,
    }
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = Question.objects.get(id=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)


def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question_id)
    else:
        form = AnswerForm()
    context = {"question": question, "form": form}
    return render(request, "pybo/question_detail.html", context)


def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    context = {"form": form}
    return render(request, "pybo/question_form.html", context)
