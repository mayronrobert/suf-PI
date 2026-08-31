from django.contrib import admin

from .models import Membro, Medico, PacienteFila

admin.site.register(Membro)
admin.site.register(Medico)
admin.site.register(PacienteFila)

# Register your models here.
