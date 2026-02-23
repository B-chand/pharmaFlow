from django.contrib import admin
from django.utils.html import format_html
from .models import Medicine, Supplier, Customer, Purchase, Sale, ContactSubmission


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'email', 'created')
    search_fields = ('name', 'email', 'phone')


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'stock', 'price', 'expiry_date', 'supplier', 'stock_badge')
    list_filter   = ('category', 'supplier')
    search_fields = ('name',)
    date_hierarchy = 'expiry_date'

    def stock_badge(self, obj):
        color = {'ok': 'green', 'low': 'orange', 'out': 'red'}[obj.stock_status]
        return format_html('<span style="color:{}">{}</span>', color, obj.stock)
    stock_badge.short_description = 'Stock Status'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ('name', 'phone', 'email', 'created')
    search_fields = ('name', 'email', 'phone')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'medicine', 'supplier', 'quantity', 'total_price', 'purchase_date')
    list_filter   = ('purchase_date', 'supplier')
    search_fields = ('medicine__name',)
    date_hierarchy = 'purchase_date'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'medicine', 'customer', 'quantity', 'total_price', 'sale_date')
    list_filter   = ('sale_date', 'customer')
    search_fields = ('medicine__name', 'customer__name')
    date_hierarchy = 'sale_date'


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'created_at', 'is_read')
    list_filter   = ('is_read',)
    search_fields = ('name', 'email')
    readonly_fields = ('name', 'email', 'message', 'created_at')

    def has_add_permission(self, request):
        return False
