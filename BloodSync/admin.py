from django.contrib import admin
from .models import Donor, BloodRequest


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'gender',
        'age',
        'blood_group',
        'phone',
        'city',
        'state',
    )

    search_fields = (
        'name',
        'blood_group',
        'city',
    )

    list_filter = (
        'blood_group',
        'city',
        'state',
    )


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'patient_name',
        'blood_group',
        'units_required',
        'hospital_name',
        'city',
        'contact_number',
    )

    search_fields = (
        'patient_name',
        'blood_group',
        'city',
    )

    list_filter = (
        'blood_group',
        'city',
    )