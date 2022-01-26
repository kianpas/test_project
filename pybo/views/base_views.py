from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import Question

MAX_LIST_CNT = 10
MAX_PAGE_CNT = 5

def index(request):
    """
    pybo 목록 출력
    """
    # page 번호
    page = request.GET.get("page", "1")
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

       # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')


    # 질문 리스트
    # question_list = Question.objects.order_by("-create_date")

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

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
        "kw": kw,
        'so': so
    }
    return render(request, "pybo/question_list.html", context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = Question.objects.get(id=question_id)
    context = {"question": question}
    return render(request, "pybo/question_detail.html", context)