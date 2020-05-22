from django.urls import path

from core.views import CentroEducativoListView

app_name = 'core'

urlpatterns = [
    path('school/search', CentroEducativoListView.as_view()),
]
