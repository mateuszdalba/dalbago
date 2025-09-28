from django.core.management.base import BaseCommand
from garage.models import GarageAllowedActivity, GarageForbiddenActivity, GarageTool

class Command(BaseCommand):
    help = "Seeds database with initial garage features, activities and tools"

    def handle(self, *args, **kwargs):
        allowed = [
            "Wymiana oleju silnikowego",
            "Wymiana oleju przekładniowego",
            "Wymiana płynu chłodniczego",
            "Wymiana płynu hamulcowego",
            "Wymiana filtrów",
            "Serwis hamulców",
            "Wymiana akumulatora",
            "Serwis zawieszenia",
            "Inna naprawa mechaniczna",
        ]
        forbidden = [
            "Mycie",
            "Lakierowanie",
            "Spawanie",
        ]
        tools = [
            "Podnośnik hydrauliczny",
            "Kanał serwisowy",
            "Zestaw kluczy nasadowych",
            "Wkrętarka elektryczna",
            "Kompresor",
            "Narzędzia do detailingu",
        ]

        for name in allowed:
            GarageAllowedActivity.objects.get_or_create(name=name)
        for name in forbidden:
            GarageForbiddenActivity.objects.get_or_create(name=name)
        for name in tools:
            GarageTool.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Garage data seeded successfully!"))
