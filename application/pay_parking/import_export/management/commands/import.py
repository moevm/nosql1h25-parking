import json
from django.core.management.base import BaseCommand
from import_export.import_data import import_data


class Command(BaseCommand):
    help = "Load ingredients from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        file_path = options["file"]

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        import_data(data)

        self.stdout.write(self.style.SUCCESS("Data loaded."))
