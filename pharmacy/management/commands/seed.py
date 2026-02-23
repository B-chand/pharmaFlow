"""
Management command: python manage.py seed
Seeds the database with example Suppliers, Medicines, and Customers.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from pharmacy.models import Supplier, Medicine, Customer


SUPPLIERS = [
    {'name': 'MedLine Global',      'phone': '+1-800-635-4633', 'email': 'orders@medline.com',    'address': '3 Lake Blvd, Northfield, IL 60093'},
    {'name': 'PharmaDirect Inc.',   'phone': '+1-888-200-6700', 'email': 'supply@pharmadirect.com','address': '120 First Ave, Atlanta, GA 30308'},
    {'name': 'HealthBridge Supply', 'phone': '+1-877-463-2584', 'email': 'info@healthbridge.io',   'address': '45 Commerce Dr, Austin, TX 78701'},
    {'name': 'CuraMed Europe',      'phone': '+44-20-7946-0800','email': 'eu@curamed.com',          'address': '14 Harley St, London W1G 9PH'},
]

MEDICINES = [
    {'name': 'Amoxicillin 500mg',    'category': 'antibiotic',    'stock': 250, 'price': '8.99',  'days': 730},
    {'name': 'Ibuprofen 400mg',      'category': 'analgesic',     'stock': 500, 'price': '5.49',  'days': 1095},
    {'name': 'Paracetamol 500mg',    'category': 'analgesic',     'stock': 600, 'price': '4.25',  'days': 900},
    {'name': 'Omeprazole 20mg',      'category': 'gastro',        'stock': 180, 'price': '12.99', 'days': 540},
    {'name': 'Cetirizine 10mg',      'category': 'respiratory',   'stock': 320, 'price': '7.75',  'days': 730},
    {'name': 'Metformin 500mg',      'category': 'diabetes',      'stock': 15,  'price': '14.50', 'days': 365},   # low stock
    {'name': 'Atorvastatin 20mg',    'category': 'cardiovascular','stock': 8,   'price': '22.00', 'days': 545},   # low stock
    {'name': 'Vitamin D3 1000IU',    'category': 'vitamin',       'stock': 0,   'price': '9.99',  'days': 365},   # out of stock
    {'name': 'Azithromycin 250mg',   'category': 'antibiotic',    'stock': 90,  'price': '18.50', 'days': -30},   # expired
    {'name': 'Hydrocortisone 1% Cream','category': 'dermatology', 'stock': 75,  'price': '6.85',  'days': 820},
    {'name': 'Salbutamol Inhaler',   'category': 'respiratory',   'stock': 40,  'price': '28.00', 'days': 600},
    {'name': 'Fluconazole 150mg',    'category': 'antifungal',    'stock': 60,  'price': '11.25', 'days': 450},
]

CUSTOMERS = [
    {'name': 'Alice Thornton',  'phone': '+1-555-0101', 'email': 'alice.t@email.com',   'address': '12 Maple St, Boston, MA'},
    {'name': 'Bob Marquez',     'phone': '+1-555-0102', 'email': 'bob.m@webmail.com',   'address': '88 Pine Ave, Miami, FL'},
    {'name': 'Carol Singh',     'phone': '+1-555-0103', 'email': 'carol.singh@live.com','address': '7 Oak Lane, Denver, CO'},
    {'name': 'David Chen',      'phone': '+1-555-0104', 'email': 'd.chen@inbox.net',    'address': '321 Elm Dr, Seattle, WA'},
    {'name': 'Eva Johansson',   'phone': '+1-555-0105', 'email': 'eva.j@nordic.se',     'address': '5 Birch Rd, Portland, OR'},
    {'name': 'Frank Okafor',    'phone': '+1-555-0106', 'email': 'f.okafor@mail.ng',    'address': '99 Cedar Blvd, Chicago, IL'},
]


class Command(BaseCommand):
    help = 'Seeds the database with example pharmacy data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('🌱 Seeding PharmaFlow database…'))

        # Suppliers
        suppliers = []
        for s in SUPPLIERS:
            obj, created = Supplier.objects.get_or_create(name=s['name'], defaults=s)
            suppliers.append(obj)
            if created:
                self.stdout.write(f"  + Supplier: {obj.name}")

        # Medicines
        today = date.today()
        for i, m in enumerate(MEDICINES):
            exp = today + timedelta(days=m.pop('days'))
            obj, created = Medicine.objects.get_or_create(
                name=m['name'],
                defaults={**m, 'expiry_date': exp, 'supplier': suppliers[i % len(suppliers)]}
            )
            if created:
                self.stdout.write(f"  + Medicine: {obj.name}")

        # Customers
        for c in CUSTOMERS:
            obj, created = Customer.objects.get_or_create(name=c['name'], defaults=c)
            if created:
                self.stdout.write(f"  + Customer: {obj.name}")

        self.stdout.write(self.style.SUCCESS('\n✅ Seed complete!'))
        self.stdout.write('   Run: python manage.py runserver')
