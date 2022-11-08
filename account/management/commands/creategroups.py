from django.core.management import BaseCommand

from account.permissions import create_groups


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_groups()
