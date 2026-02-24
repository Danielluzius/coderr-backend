import shutil
from pathlib import Path

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from offers_app.models import Offer, OfferDetail
from profiles_app.models import UserProfile
from reviews_app.models import Review


FRONTEND_ASSETS = Path(__file__).resolve().parent.parent.parent.parent.parent / 'frontend' / 'assets' / 'img'
MEDIA_ROOT = Path(__file__).resolve().parent.parent.parent.parent / 'media'


def copy_image(src_relative, dest_subdir, dest_filename):
    """Copies an image from the frontend assets to the media folder and returns the relative media path."""
    src = FRONTEND_ASSETS / src_relative
    dest_dir = MEDIA_ROOT / dest_subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / dest_filename
    if src.exists():
        shutil.copy2(src, dest)
    return f'{dest_subdir}/{dest_filename}'


class Command(BaseCommand):
    help = 'Creates demo users, profiles, offers and reviews for development.'

    def handle(self, *args, **options):
        self.stdout.write('=== Demo-Daten werden erstellt ===\n')

        kevin, kevin_created = self._get_or_create_user(
            username='kevin',
            password='asdasd24',
            email='kevin@demo.com',
            first_name='Kevin',
            last_name='Müller',
        )
        kevin_profile, _ = UserProfile.objects.get_or_create(user=kevin, defaults={'type': 'business'})
        kevin_profile.file = copy_image('landingpage/person_1.png', 'profile_pictures', 'kevin.png')
        kevin_profile.location = 'Berlin'
        kevin_profile.tel = '+49 30 123456'
        kevin_profile.description = 'Ich bin ein erfahrener Grafikdesigner mit über 10 Jahren Berufserfahrung.'
        kevin_profile.working_hours = 'Mo-Fr 9-18 Uhr'
        kevin_profile.type = 'business'
        kevin_profile.save()
        self._log_created('Business-User kevin', kevin_created)

        anna, anna_created = self._get_or_create_user(
            username='anna',
            password='asdasd24',
            email='anna@demo.com',
            first_name='Anna',
            last_name='Schmidt',
        )
        anna_profile, _ = UserProfile.objects.get_or_create(user=anna, defaults={'type': 'business'})
        anna_profile.file = copy_image('landingpage/person_2.png', 'profile_pictures', 'anna.png')
        anna_profile.location = 'München'
        anna_profile.tel = '+49 89 654321'
        anna_profile.description = 'Webentwicklerin mit Fokus auf moderne Frontend-Technologien.'
        anna_profile.working_hours = 'Mo-Do 8-17 Uhr'
        anna_profile.type = 'business'
        anna_profile.save()
        self._log_created('Business-User anna', anna_created)

        andrey, andrey_created = self._get_or_create_user(
            username='andrey',
            password='asdasd',
            email='andrey@demo.com',
            first_name='Andrey',
            last_name='Petrov',
        )
        andrey_profile, _ = UserProfile.objects.get_or_create(user=andrey, defaults={'type': 'customer'})
        andrey_profile.file = copy_image('landingpage/person_3.png', 'profile_pictures', 'andrey.png')
        andrey_profile.type = 'customer'
        andrey_profile.save()
        self._log_created('Customer-User andrey', andrey_created)

        lisa, lisa_created = self._get_or_create_user(
            username='lisa',
            password='asdasd24',
            email='lisa@demo.com',
            first_name='Lisa',
            last_name='Weber',
        )
        lisa_profile, _ = UserProfile.objects.get_or_create(user=lisa, defaults={'type': 'customer'})
        lisa_profile.file = copy_image('landingpage/person_4.png', 'profile_pictures', 'lisa.png')
        lisa_profile.type = 'customer'
        lisa_profile.save()
        self._log_created('Customer-User lisa', lisa_created)

        offer1, offer1_created = Offer.objects.get_or_create(
            user=kevin,
            title='Logo Design',
            defaults={
                'description': 'Professionelles Logo-Design für dein Unternehmen – modern, einzigartig und skalierbar.',
                'image': copy_image('placeholder.jpg', 'offer_images', 'logo_design.jpg'),
            },
        )
        if offer1_created:
            OfferDetail.objects.bulk_create([
                OfferDetail(offer=offer1, title='Basic Logo', offer_type='basic', price=99.00, delivery_time_in_days=5, revisions=2, features=['1 Konzept', 'PNG & JPG', '2 Revisionen']),
                OfferDetail(offer=offer1, title='Standard Logo', offer_type='standard', price=199.00, delivery_time_in_days=3, revisions=5, features=['3 Konzepte', 'PNG, JPG & SVG', '5 Revisionen', 'Quelldatei']),
                OfferDetail(offer=offer1, title='Premium Logo', offer_type='premium', price=349.00, delivery_time_in_days=2, revisions=-1, features=['5 Konzepte', 'Alle Formate', 'Unbegrenzte Revisionen', 'Quelldatei', 'Branding-Guide']),
            ])
        self._log_created('Angebot "Logo Design"', offer1_created)

        offer2, offer2_created = Offer.objects.get_or_create(
            user=kevin,
            title='Social Media Design',
            defaults={
                'description': 'Ansprechende Grafiken für Instagram, Facebook und Co.',
                'image': copy_image('placeholder.jpg', 'offer_images', 'social_media.jpg'),
            },
        )
        if offer2_created:
            OfferDetail.objects.bulk_create([
                OfferDetail(offer=offer2, title='Starter Paket', offer_type='basic', price=59.00, delivery_time_in_days=3, revisions=2, features=['5 Posts', '2 Revisionen']),
                OfferDetail(offer=offer2, title='Business Paket', offer_type='standard', price=129.00, delivery_time_in_days=2, revisions=4, features=['15 Posts', '4 Revisionen', 'Story-Format']),
                OfferDetail(offer=offer2, title='Premium Paket', offer_type='premium', price=229.00, delivery_time_in_days=1, revisions=-1, features=['30 Posts', 'Unbegrenzte Revisionen', 'Story & Reels', 'Branding']),
            ])
        self._log_created('Angebot "Social Media Design"', offer2_created)

        offer3, offer3_created = Offer.objects.get_or_create(
            user=anna,
            title='Website Entwicklung',
            defaults={
                'description': 'Moderne, responsive Webseiten mit HTML, CSS und JavaScript.',
                'image': copy_image('placeholder.jpg', 'offer_images', 'website.jpg'),
            },
        )
        if offer3_created:
            OfferDetail.objects.bulk_create([
                OfferDetail(offer=offer3, title='Landing Page', offer_type='basic', price=299.00, delivery_time_in_days=7, revisions=2, features=['1 Seite', 'Responsive', '2 Revisionen']),
                OfferDetail(offer=offer3, title='Business Website', offer_type='standard', price=599.00, delivery_time_in_days=14, revisions=5, features=['5 Seiten', 'Responsive', 'Kontaktformular', '5 Revisionen']),
                OfferDetail(offer=offer3, title='Premium Website', offer_type='premium', price=999.00, delivery_time_in_days=21, revisions=-1, features=['10 Seiten', 'CMS Integration', 'SEO-Optimierung', 'Unbegrenzte Revisionen']),
            ])
        self._log_created('Angebot "Website Entwicklung"', offer3_created)

        rev1, rev1_created = Review.objects.get_or_create(
            business_user=kevin,
            reviewer=andrey,
            defaults={
                'rating': 5,
                'description': 'Absolut top! Kevin hat mein Logo genau nach meinen Vorstellungen umgesetzt. Sehr professionell und schnell.',
            },
        )
        self._log_created('Review andrey → kevin', rev1_created)

        rev2, rev2_created = Review.objects.get_or_create(
            business_user=kevin,
            reviewer=lisa,
            defaults={
                'rating': 4,
                'description': 'Sehr gute Arbeit, das Design ist modern und ansprechend. Kleine Anpassungen wurden schnell umgesetzt.',
            },
        )
        self._log_created('Review lisa → kevin', rev2_created)

        rev3, rev3_created = Review.objects.get_or_create(
            business_user=anna,
            reviewer=andrey,
            defaults={
                'rating': 5,
                'description': 'Die Website ist wunderbar geworden! Anna arbeitet sehr strukturiert und kommuniziert klar.',
            },
        )
        self._log_created('Review andrey → anna', rev3_created)

        self.stdout.write(self.style.SUCCESS('\n=== Fertig! Demo-Daten wurden erfolgreich angelegt. ==='))

    def _get_or_create_user(self, username, password, email, first_name, last_name):
        if User.objects.filter(username=username).exists():
            return User.objects.get(username=username), False
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        return user, True

    def _log_created(self, label, created):
        if created:
            self.stdout.write(f'  ✔ {label} erstellt')
        else:
            self.stdout.write(f'  – {label} existiert bereits, übersprungen')
