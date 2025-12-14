from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Seed the database with sample listing data"
    def handle(self,*args,**kwargs):
         self.stdout.write("seeding database ...")
         host , created = User.objects.get_or_create(
            email="host@example.com"
            passwword="your_password"
         )
         sample_locations = ["Casablanca", "Rabat", "Marrakech", "Tangier", "Agadir"]
         sample_titles = [
            "Luxury Apartment",
            "Beach House",
            "City Center Studio",
            "Traditional Riad",
            "Modern Villa",
            ]
        for i in range(10):
            listings.objects.create(
                host=host,
                title=random.choice(sample_titles),
                description="Sample description for listing number " + str(i),
                price_per_night=random.randint(30, 200),
                location=random.choice(sample_locations),
            )
  
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))


