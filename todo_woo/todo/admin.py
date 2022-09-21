from django.contrib import admin
from .models import Todo

class TodoController(admin.ModelAdmin):
    readonly_fields = ('created',) 

admin.site.register(Todo, TodoController)  

