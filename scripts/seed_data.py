import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jango.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
from membros.models import Medico, PacienteFila
from django.utils import timezone as tz

User = get_user_model()
username = 'mayron'
user = User.objects.filter(username=username).first()
print('user found:', bool(user))
if not user:
    print('No user "{}" found. Existing users:'.format(username))
    print([u.username for u in User.objects.all()])
else:
    medico, created = Medico.objects.get_or_create(usuario=user, defaults={'nome_completo': 'Dr Teste', 'especialidade': 'Geral'})
    print('Medico:', medico, 'created:', created)
    existing = PacienteFila.objects.filter(medico_destinado=medico).count()
    print('existing pacientes for medico:', existing)
    if existing == 0:
        for i in range(1, 4):
            PacienteFila.objects.create(nome=f'Paciente {i}', senha=f'S{i:03d}', medico_destinado=medico, horario_chegada=tz.now())
        print('3 pacientes criados')
    else:
        print('Não criou; já existem pacientes')
