from django.contrib import admin

# Регистрируем модели в административной панели

from .models import Choice, Question

# Inline для выбора вариантов ответа (Choice) в админке
class ChoiceInline(admin.TabularInline):
    model = Choice  # Модель, которая будет отображаться в виде инлайна
    extra = 3  # Количество пустых форм для добавления вариантов ответа по умолчанию

# Настройки отображения модели Question в административной панели
class QuestionAdmin(admin.ModelAdmin):
    # Определяем, как будут отображаться поля в форме редактирования вопроса
    fieldsets = [
        (None, {"fields": ["question_text"]}),  # Основное поле для текста вопроса
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),  # Поле для даты публикации (скрыто в разделе "Date information")
    ]
    # Включаем инлайн для выбора вариантов ответа (Choice)
    inlines = [ChoiceInline]
    
    # Настройка отображения полей в списке вопросов на странице администрирования
    list_display = ["question_text", "pub_date"]  # Отображаем текст вопроса и дату публикации
    list_display = ["question_text", "pub_date", "was_published_recently"]  # Добавляем метод was_published_recently для отображения статуса публикации
    list_filter = ["pub_date"]  # Фильтрация списка вопросов по дате публикации

# Регистрируем модель Question с настроенной админской конфигурацией
admin.site.register(Question, QuestionAdmin)
