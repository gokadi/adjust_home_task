import csv
import os
from argparse import ArgumentParser

from django.conf import settings
from django.core.management import BaseCommand

from adjust_home_task.statistics.models import Statistics


class Command(BaseCommand):
    help = "Read dataset in csv format and load data into DB"

    def handle(self, *args, **options):
        from_file = options["from_file"]
        created_entries_amount = 0
        general_entries_amount = 0
        with open(from_file) as data_file:
            reader = csv.reader(data_file, delimiter=',')
            next(reader)  # skip headings
            for row in reader:
                general_entries_amount += 1
                # In future this may lead to performance issues.
                # Than use 'bulk_create'
                statistics, is_created = Statistics.objects.get_or_create(
                    date=row[0],
                    channel=row[1],
                    country=row[2],
                    os=row[3],
                    impressions=row[4],
                    clicks=row[5],
                    installs=row[6],
                    spend=row[7],
                    revenue=row[8],
                )
                if is_created:
                    created_entries_amount += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Created: `{created_entries_amount}` statistics '
                f'entries from `{general_entries_amount}`.'
            )
        )

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "--from",
            dest="from_file",
            default=os.path.join(
                settings.BASE_DIR,
                "adjust_home_task/statistics/management/data/dataset.csv"
            ),
            help="path to dataset file",
        )
