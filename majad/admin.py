from django.contrib import admin

# Register your models here.
from majad.models import Coordinador, CentroReferencia


@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    pass


@admin.register(CentroReferencia)
class CentroReferenciaAdmin(admin.ModelAdmin):
    pass
