#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    # Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE, указывающую на настройки проекта Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    
    try:
        # Импортируем функцию для выполнения команд Django через командную строку
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обработка исключения в случае, если Django не установлен или неправильно настроен
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Выполняем команду, переданную в аргументах командной строки
    execute_from_command_line(sys.argv)


# Если скрипт запускается как основной, вызываем функцию main()
if __name__ == '__main__':
    main()
