from django.urls import path

from core.views import (
    AlumnoModelViewSet,
    AlumnoDetailView
)
from majad.views import (
    AdministradorListCreateView,
    AdministradorDetailView,
    CoordinadorListCreateView,
    CoordinadorDetailView,
    CentroReferenciaListCreateView,
    CentroReferenciaDetailView,
    ClaseListCreateView,
    ClaseDetailView,
    MallaCurricularListCreateView,
    MallaCurricularDetailView,
    GradoListCreateView,
    GradoDetailView,
    PeriodoDetailView,
    PeriodoListCreateView,
    UserListView,
    UserDetailView,
    MatriculaListCreateView
)

app_name = 'majad'

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/<int:pk>', UserDetailView.as_view()),

    path('administrator/', AdministradorListCreateView.as_view()),
    path('administrator/<int:pk>', AdministradorDetailView.as_view()),

    path('coordinator/', CoordinadorListCreateView.as_view()),
    path('coordinator/<int:pk>', CoordinadorDetailView.as_view()),

    path('reference/school/', CentroReferenciaListCreateView.as_view()),
    path('reference/school/<int:pk>', CentroReferenciaDetailView.as_view()),

    path('clase/', ClaseListCreateView.as_view()),
    path('clase/<int:pk>', ClaseDetailView.as_view()),

    path('malla/', MallaCurricularListCreateView.as_view()),
    path('malla/<int:pk>', MallaCurricularDetailView.as_view()),

    path('grado/', GradoListCreateView.as_view()),
    path('grado/<int:pk>', GradoDetailView.as_view()),

    path('periodo/', PeriodoListCreateView.as_view()),
    path('periodo/<int:pk>', PeriodoDetailView.as_view()),

    path('alumno/', AlumnoModelViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('alumno/<int:pk>', AlumnoModelViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('alumno/identity/<str:identity>', AlumnoDetailView.as_view()),

    path('matricula/', MatriculaListCreateView.as_view()),
]
