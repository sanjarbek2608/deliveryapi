from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Restaurant, Menu, Order

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Order)


