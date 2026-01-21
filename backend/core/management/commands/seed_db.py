import itertools
import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Company
from parts.models import Designator, Part
from inventory.models import Storage, Stock


def generate_storage_codes():
    """Generate storage codes from patterns: SM0[1-6]-[1-5][A-F] and LG0[1-3]-[1-3][A-C]"""
    codes = []
    for shelf in range(1, 7):
        for pos in range(1, 6):
            for row in "ABCDEF":
                codes.append(f"SM0{shelf}-{pos}{row}")
    for shelf in range(1, 4):
        for pos in range(1, 4):
            for row in "ABC":
                codes.append(f"LG0{shelf}-{pos}{row}")
    return sorted(codes)


class Command(BaseCommand):
    help = "Seed database from data/ directory files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--companies",
            action="store_true",
            help="Seed companies from data/companies.json",
        )
        parser.add_argument(
            "--designators",
            action="store_true",
            help="Seed designators from data/designators.json",
        )
        parser.add_argument(
            "--parts",
            action="store_true",
            help="Seed parts from data/parts.csv",
        )
        parser.add_argument(
            "--storage",
            action="store_true",
            help="Generate storage locations",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Seed all data (companies, designators, storage, parts)",
        )

    def handle(self, *args, **options):
        data_dir = Path.cwd() / "data"

        seed_companies = options["companies"] or options["all"]
        seed_designators = options["designators"] or options["all"]
        seed_storage = options["storage"] or options["all"]
        seed_parts = options["parts"] or options["all"]

        if not (seed_companies or seed_designators or seed_storage or seed_parts):
            seed_companies = seed_designators = seed_storage = seed_parts = True

        with transaction.atomic():
            if seed_companies:
                self.seed_companies(data_dir / "companies.json")
            if seed_designators:
                self.seed_designators(data_dir / "designators.json")
            if seed_storage:
                self.seed_storage()
            if seed_parts:
                self.seed_parts(data_dir / "parts.csv")

    def seed_companies(self, filepath: Path):
        self.stdout.write(f"Seeding companies from {filepath}...")

        with open(filepath, "r") as f:
            companies = json.load(f)

        created = 0
        for company_data in companies:
            company, was_created = Company.objects.update_or_create(
                name=company_data["name"],
                defaults={
                    "website": company_data.get("website", ""),
                    "is_manufacturer": company_data.get("is_manufacturer", False),
                    "is_vendor": company_data.get("is_vendor", False),
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} companies"))

    def seed_designators(self, filepath: Path):
        self.stdout.write(f"Seeding designators from {filepath}...")

        with open(filepath, "r") as f:
            designators = json.load(f)

        created = 0
        for desig_data in designators:
            desig, was_created = Designator.objects.update_or_create(
                code=desig_data["code"],
                defaults={"name": desig_data["name"]},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} designators"))

    def seed_storage(self):
        self.stdout.write("Generating storage locations...")

        codes = generate_storage_codes()
        created = 0

        for code in codes:
            storage, was_created = Storage.objects.get_or_create(
                name=code,
                defaults={"description": f"Storage bin: {code}"},
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} storage locations"))

    def seed_parts(self, filepath: Path):
        self.stdout.write(f"Seeding parts from {filepath}...")

        default_storage, _ = Storage.objects.get_or_create(
            name="Default",
            defaults={"description": "Default storage location"},
        )

        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            created_parts = 0
            created_stock = 0

            for row in reader:
                name = row.get("Name", "").strip()
                inventory = int(row.get("Inventory", 0) or 0)
                description = row.get("Description", "").strip()
                manufacturer_name = row.get("Manufacturer", "").strip()
                designator_code = row.get("Designator", "").strip().upper()[:3]
                location = row.get("Location", "").strip()

                if not name:
                    continue

                designator = None
                if designator_code:
                    designator = Designator.objects.filter(code=designator_code).first()

                manufacturer = None
                if manufacturer_name:
                    manufacturer = Company.objects.filter(name=manufacturer_name, is_manufacturer=True).first()

                part, part_created = Part.objects.update_or_create(
                    name=name,
                    defaults={
                        "description": description,
                        "designator": designator,
                        "manufacturer": manufacturer,
                    },
                )

                if part_created:
                    created_parts += 1

                if inventory > 0:
                    storage = default_storage
                    if location:
                        storage, _ = Storage.objects.get_or_create(
                            name=location,
                            defaults={"description": f"Storage location: {location}"},
                        )

                    stock, stock_created = Stock.objects.update_or_create(
                        part=part,
                        storage=storage,
                        defaults={"quantity": inventory, "status": None},
                    )
                    if stock_created:
                        created_stock += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created_parts} parts, {created_stock} stock entries"))
