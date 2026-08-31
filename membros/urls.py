from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_medico, name='dashboard_medico'),
    path('dashboard/atualizar/', views.atualizar_fila_fragmento, name='atualizar_fila_fragmento'),
    path('chamar/<int:paciente_id>/', views.chamar_paciente, name='chamar_paciente'),
    path('finalizar/<int:paciente_id>/', views.finalizar_atendimento, name='finalizar_atendimento'),
    
    path('cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('cliente/atualizar/', views.atualizar_cliente_fragmento, name='atualizar_cliente_fragmento'),
    path('paciente/', views.paciente_publico, name='paciente_publico'),
    path('paciente/agendar/', views.agendar_paciente, name='agendar_paciente'),
]
