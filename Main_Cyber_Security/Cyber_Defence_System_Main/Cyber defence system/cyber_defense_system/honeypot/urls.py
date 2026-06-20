from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('honeypot-login/', views.honeypot_login, name='honeypot_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logs/', views.attack_logs, name='attack_logs'),
    path('previous-logs/', views.previous_logs, name='previous_logs'),
    path('attacker-types/', views.attacker_types, name='attacker_types'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
