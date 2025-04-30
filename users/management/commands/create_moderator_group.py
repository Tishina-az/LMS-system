from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор" и назначает ей необходимые разрешения'

    def handle(self, *args, **options):
        group, create = Group.objects.get_or_create(name='Модератор')

        if create:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор" успешно создана.'))

            view_course_permission = Permission.objects.get(codename='view_course')
            view_lesson_permission = Permission.objects.get(codename='view_lesson')
            change_course_permission = Permission.objects.get(codename='change_course')
            change_lesson_permission = Permission.objects.get(codename='change_lesson')

            group.permissions.add(view_course_permission, view_lesson_permission, change_course_permission,
                                  change_lesson_permission)
            self.stdout.write(self.style.SUCCESS('Группе "Модератор" успешно назначены разрешения'))

        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор" уже существует.'))
