from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
# admin.site.register(CarMake)
admin.site.register(CarModel)

 
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3
# CarModelAdmin class


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register models here
# admin.site.register(CarMake)
admin.site.register(CarMake, CarMakeAdmin)
