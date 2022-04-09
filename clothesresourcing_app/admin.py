from django.contrib import admin
from clothesresourcing_app.models import Donation, Institution, Category

# Register your models here.

admin.site.register(Category)

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "type")
    search_fields = ("name__startswith",)

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("user", "institution", "quantity")



