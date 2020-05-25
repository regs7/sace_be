from django.urls import path

from core.views import CentroEducativoListView, MunicipioListView

app_name = 'core'

urlpatterns = [
    path('school/search', CentroEducativoListView.as_view()),
    path('municipio/search', MunicipioListView.as_view()),
]
