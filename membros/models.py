from django.db import models
from django.contrib.auth.models import User

class Membro(models.Model):

 nome_completo = models.CharField(
 max_length=200,
 verbose_name="Nome Completo"  
  )

 email = models.EmailField(
 unique=True,
 verbose_name="E-mail"

)

telefone = models.CharField(
 
 max_length=20,
 blank=True,
 null= True,

) 
data_cadastro = models.DateField(
    auto_now_add=True,
    verbose_name="Data de Cadastro"

) 
status = models.BooleanField(
    default=True,
    verbose_name="Ativo"

)
    
TIPO_CHOICES = [
    ('voluntario', 'Voluntário'),
    ('doador', 'Doador'),
    ('parceiro', 'Parceiro'),
]
tipo_membro = models.CharField(
    max_length=50,
    choices=TIPO_CHOICES,
    default='voluntario',
    verbose_name="Tipo de Membro"
)

def __str__(self):
    return self.nome_completo

class Meta:
    verbose_name = "Membro"
    verbose_name_plural = "Membros"
    ordering = ['nome_completo']


class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_completo


class PacienteFila(models.Model):
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando'),
        ('em_atendimento', 'Em Atendimento'),
        ('finalizado', 'Finalizado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultas')
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, blank=True, default='')
    senha = models.CharField(max_length=10)
    medico_destinado = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='pacientes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando')
    horario_chegada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['horario_chegada']

    def __str__(self):
        return f"{self.senha} - {self.nome}"