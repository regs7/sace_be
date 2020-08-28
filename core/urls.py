from django.urls import path

from core.views import (
    CentroEducativoListView,
    MunicipioListView,
    StudentTuitionListView
)

app_name = 'core'

urlpatterns = [
    path('school/search', CentroEducativoListView.as_view()),
    path('municipio/search', MunicipioListView.as_view()),
    path('student/tuition/search', StudentTuitionListView.as_view()),
]
