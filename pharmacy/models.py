"""
PharmaFlow Models
-----------------
Medicine · Supplier · Customer · Purchase · Sale · ContactSubmission
"""
from django.db import models
from django.utils import timezone


# ─── Supplier ─────────────────────────────────────────────────────────────────
class Supplier(models.Model):
    name    = models.CharField(max_length=200)
    phone   = models.CharField(max_length=30, blank=True)
    email   = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ─── Medicine ─────────────────────────────────────────────────────────────────
class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('antibiotic',    'Antibiotic'),
        ('analgesic',     'Analgesic / Pain Relief'),
        ('antiviral',     'Antiviral'),
        ('antifungal',    'Antifungal'),
        ('antiseptic',    'Antiseptic'),
        ('vitamin',       'Vitamin / Supplement'),
        ('cardiovascular','Cardiovascular'),
        ('dermatology',   'Dermatology'),
        ('gastro',        'Gastrointestinal'),
        ('respiratory',   'Respiratory'),
        ('diabetes',      'Diabetes / Endocrine'),
        ('other',         'Other'),
    ]

    name        = models.CharField(max_length=200)
    category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    stock       = models.PositiveIntegerField(default=0)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()
    supplier    = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='medicines'
    )
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    # ── Computed helpers ──
    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 20

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    @property
    def stock_status(self):
        if self.is_out_of_stock:
            return 'out'
        if self.is_low_stock:
            return 'low'
        return 'ok'


# ─── Customer ─────────────────────────────────────────────────────────────────
class Customer(models.Model):
    name    = models.CharField(max_length=200)
    phone   = models.CharField(max_length=30, blank=True)
    email   = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ─── Purchase (stock IN) ──────────────────────────────────────────────────────
class Purchase(models.Model):
    medicine      = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='purchases')
    supplier      = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity      = models.PositiveIntegerField()
    total_price   = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now)
    notes         = models.TextField(blank=True)
    created       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-purchase_date', '-created']

    def __str__(self):
        return f"Purchase #{self.pk} – {self.medicine} ({self.quantity} units)"

    def save(self, *args, **kwargs):
        """Auto-increase medicine stock on new purchase."""
        is_new = self.pk is None
        if is_new:
            old_qty = 0
        else:
            old_qty = Purchase.objects.get(pk=self.pk).quantity
        super().save(*args, **kwargs)
        if is_new:
            Medicine.objects.filter(pk=self.medicine_id).update(
                stock=models.F('stock') + self.quantity
            )
        else:
            diff = self.quantity - old_qty
            Medicine.objects.filter(pk=self.medicine_id).update(
                stock=models.F('stock') + diff
            )


# ─── Sale (stock OUT) ─────────────────────────────────────────────────────────
class Sale(models.Model):
    medicine    = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='sales')
    customer    = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity    = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date   = models.DateField(default=timezone.now)
    notes       = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sale_date', '-created']

    def __str__(self):
        return f"Sale #{self.pk} – {self.medicine} ({self.quantity} units)"

    def save(self, *args, **kwargs):
        """Auto-decrease medicine stock on new sale."""
        is_new = self.pk is None
        old_qty = 0
        if not is_new:
            old_qty = Sale.objects.get(pk=self.pk).quantity
        super().save(*args, **kwargs)
        if is_new:
            Medicine.objects.filter(pk=self.medicine_id).update(
                stock=models.F('stock') - self.quantity
            )
        else:
            diff = self.quantity - old_qty
            Medicine.objects.filter(pk=self.medicine_id).update(
                stock=models.F('stock') - diff
            )


# ─── Contact Submission ───────────────────────────────────────────────────────
class ContactSubmission(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Contact from {self.name} ({self.email})"
