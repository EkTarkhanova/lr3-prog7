from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

# Представление для отображения списка последних пяти вопросов
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Возвращает последние пять опубликованных вопросов."""
        return Question.objects.order_by("-pub_date")[:5]


# Представление для отображения подробной информации о вопросе
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Исключает все вопросы, которые ещё не были опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# Представление для отображения результатов голосования по вопросу
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# Представление для отображения списка последних пяти вопросов (не используя класс)
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

# Представление для отображения подробной информации о выбранном вопросе
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

# Представление для отображения результатов голосования по вопросу
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

# Представление для обработки голосования по вопросу
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Получаем выбранный вариант ответа
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Если выбор не сделан, повторно отображаем форму голосования с сообщением об ошибке
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # Увеличиваем количество голосов на 1 с использованием F-объекта для атомарных операций
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # После обработки POST-запроса всегда перенаправляем на страницу с результатами голосования
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# Дополнительный метод get_queryset, для получения последних пяти опубликованных вопросов,
# исключая те, которые еще не опубликованы
def get_queryset(self):
    """
    Возвращает последние пять опубликованных вопросов (не включая те, которые
    должны быть опубликованы в будущем).
    """
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
