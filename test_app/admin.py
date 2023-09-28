from django.contrib import admin
from .models import *

# admin.site.register(MyData)
# admin.site.register(CustomerData)


class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'Email', 'status')

# Register the model with the custom admin class
admin.site.register(CustomerData, YourModelAdmin)


class YourModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')

# Register the model with the custom admin class
admin.site.register(MyData, YourModelAdmin)