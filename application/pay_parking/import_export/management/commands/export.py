import json
from django.core.management.base import BaseCommand
from import_export.export_data import export_data


class Command(BaseCommand):
    help = "Load ingredients from a JSON file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        file_path = options["file"]
        data = export_data()
        
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS("Data uploaded."))
