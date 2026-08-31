from django import forms
from .models import Membros

class MembrosForm(forms.ModelForm):
    class Meta:
        model = Membros
        fields = ['names', 'email', 'categoria_do_membro', 'telefone', 'situacao', 'data_de_cadastro']
        
        widgets = {
            'data_de_cadastro': forms.DateInput(attrs={'type': 'date'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'})
        }
        
        labels = {
            'names': 'Nome Completo',
            'email': 'E-mail',
            'categoria_do_membro': 'Categoria do Membro',
            'telefone': 'Telefone',
            'situacao': 'Situação',
            'data_de_cadastro': 'Data de Cadastro'
        }
