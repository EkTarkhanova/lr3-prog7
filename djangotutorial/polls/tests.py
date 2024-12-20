import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


# Тесты для модели Question
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвращает False для вопросов, у которых дата публикации
        находится в будущем.
        """
        time = timezone.now() + datetime.timedelta(days=30)  # Вопрос с будущей датой
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() возвращает False для вопросов, у которых дата публикации
        старше одного дня.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)  # Вопрос старше одного дня
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() возвращает True для вопросов, у которых дата публикации
        находится в пределах последнего дня.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)  # Вопрос, опубликованный недавно
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# Функция для создания вопросов с заданным текстом и сдвигом даты публикации
def create_question(question_text, days):
    """
    Создает вопрос с заданным текстом и датой публикации, сдвинутой на заданное количество дней
    (отрицательные значения для вопросов, опубликованных в прошлом, положительные - для будущих).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# Тесты для представления индекса вопросов
class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        Если вопросов нет, отображается соответствующее сообщение.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус 200 (OK)
        self.assertContains(response, "No polls are available.")  # Проверяем, что отображается сообщение
        self.assertQuerySetEqual(response.context["latest_question_list"], [])  # Проверяем, что список вопросов пуст

    def test_past_question(self):
        """
        В представлении детализированного вопроса для вопроса, опубликованного в прошлом,
        отображается текст вопроса.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)  # Проверяем, что текст вопроса отображается

    def test_future_question(self):
        """
        В представлении детализированного вопроса для вопроса, опубликованного в будущем,
        возвращается ошибка 404 (страница не найдена).
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # Проверяем, что возвращается ошибка 404

    def test_future_question_and_past_question(self):
        """
        Даже если существуют как прошлые, так и будущие вопросы, отображаются только прошлые вопросы.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],  # В отображении должны быть только прошлые вопросы
        )

    def test_two_past_questions(self):
        """
        На странице индекса могут отображаться несколько вопросов.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],  # Проверяем, что вопросы отображаются в правильном порядке (от нового к старому)
        )
