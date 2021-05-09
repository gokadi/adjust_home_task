from django.core.management import BaseCommand

from adjust_home_task.statistics.models import Statistics


class Command(BaseCommand):
    help = "Remove all statistics entries in the database"

    def handle(self, *args, **options):
        general_entries_amount = Statistics.objects.count()
        Statistics.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Removed: `{general_entries_amount}` statistics entries.'
            )
        )
