

from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.get_companies, name='get_companies'),
    path('run-dtw/', views.run_dtw_api, name='run_dtw_api'),
    path('run-clustering/', views.run_clustering_api, name='run_clustering_api'),
    
]