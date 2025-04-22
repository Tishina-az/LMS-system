import os

from django.core.management import call_command
from django.core.management.base import BaseCommand

from config import settings
from materials.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из фикстуры'

    def handle(self, *args, **options):
        User.objects.all().delete()
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        fixture_path = os.path.join(settings.BASE_DIR, 'users', 'fixtures', 'test_data.json')

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR('Файл с фикстурой не найден!'))
            return

        try:
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка загрузки данных: {e}'))
