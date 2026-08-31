from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import Membro, PacienteFila, Medico


def dashboard(request):     
    total = Membro.objects.count()
    ativos = Membro.objects.filter(status=True).count()
    inativos = Membro.objects.filter(status=False).count()
    if total > 0:
        percentual = (ativos / total) * 100
    else:
        percentual = 0
    context = {         
        'total': total,         
        'ativos': ativos,         
        'inativos': inativos,         
        'percentual': percentual,     
    }     
    return render(request, 'dashboard.html', context)


def obter_dados_fila(user):
    medico_atual = get_object_or_404(Medico, usuario=user)
    proximo_geral = PacienteFila.objects.filter(status='aguardando').first()
    
    eh_meu_paciente = False
    if proximo_geral and proximo_geral.medico_destinado == medico_atual:
        eh_meu_paciente = True

    minha_fila_exclusiva = PacienteFila.objects.filter(
        medico_destinado=medico_atual, 
        status='aguardando'
    )
    hoje = timezone.now().date()
    historico_hoje = PacienteFila.objects.filter(
        medico_destinado=medico_atual,
        status='finalizado',
        horario_chegada__date=hoje
    ).order_by('-horario_chegada')

    # paciente atualmente em atendimento no consultório (se houver)
    max_atendendo = PacienteFila.objects.filter(
        medico_destinado=medico_atual,
        status='em_atendimento'
    ).first()
    em_atendimento_count = PacienteFila.objects.filter(medico_destinado=medico_atual, status='em_atendimento').count()
    minha_fila_count = minha_fila_exclusiva.count()

    return {
        'medico': medico_atual,
        'proximo': proximo_geral,
        'eh_meu_paciente': eh_meu_paciente,
        'minha_fila': minha_fila_exclusiva,
        'historico': historico_hoje,
        'max_atendendo': max_atendendo,
        'em_atendimento_count': em_atendimento_count,
        'minha_fila_count': minha_fila_count,
    }


@login_required
def dashboard_medico(request):
    try:
        context = obter_dados_fila(request.user)
    except Http404:
        return redirect('dashboard_cliente')
    return render(request, 'dashboard_medico.html', context)


@login_required
def atualizar_fila_fragmento(request):
    context = obter_dados_fila(request.user)
    return render(request, 'conteudo_fila.html', context)


@login_required
def chamar_paciente(request, paciente_id):
    paciente = get_object_or_404(PacienteFila, id=paciente_id)
    paciente.status = 'em_atendimento'
    paciente.save()
    return redirect('dashboard_medico')


@login_required
def finalizar_atendimento(request, paciente_id):
    paciente = get_object_or_404(PacienteFila, id=paciente_id)
    paciente.status = 'finalizado'
    paciente.save()
    return redirect('dashboard_medico')


# ------------------ VIEWS DO CLIENTE ------------------
def obter_dados_cliente(user):
    nome_completo = (user.get_full_name() or '').strip()
    username = (user.username or '').strip()

    filtro = Q(usuario=user)
    if nome_completo:
        filtro |= Q(nome__iexact=nome_completo)
    if username:
        filtro |= Q(nome__iexact=username)

    pacientes_usuario = PacienteFila.objects.filter(filtro).distinct().order_by('-horario_chegada')

    meu_atendimento_atual = pacientes_usuario.filter(status__in=['aguardando', 'em_atendimento']).first()

    posicao_fila = 0
    if meu_atendimento_atual and meu_atendimento_atual.status == 'aguardando':
        posicao_fila = PacienteFila.objects.filter(
            status='aguardando',
            horario_chegada__lte=meu_atendimento_atual.horario_chegada,
            medico_destinado=meu_atendimento_atual.medico_destinado,
        ).count()

    historico_cliente = pacientes_usuario.filter(status='finalizado').order_by('-horario_chegada')
    agenda_cliente = pacientes_usuario.order_by('-horario_chegada')

    concluidos_count = historico_cliente.count()

    AVG_MIN_PER_PATIENT = 10
    estimated_minutes = None
    if meu_atendimento_atual and meu_atendimento_atual.status == 'aguardando':
        estimated_minutes = max(0, (posicao_fila - 1) * AVG_MIN_PER_PATIENT)

    telefone = None
    from .models import Membro
    try:
        membro = Membro.objects.filter(nome_completo=nome_completo).first()
        if membro and membro.telefone:
            telefone = membro.telefone
    except Exception:
        telefone = None

    medico_associado = None
    if meu_atendimento_atual:
        medico_associado = getattr(meu_atendimento_atual, 'medico_destinado', None)

    return {
        'atual': meu_atendimento_atual,
        'posicao': posicao_fila,
        'historico': historico_cliente,
        'agenda': agenda_cliente,
        'concluidos_count': concluidos_count,
        'estimated_minutes': estimated_minutes,
        'telefone': telefone,
        'medico': medico_associado,
    }


@login_required
def dashboard_cliente(request):
    context = obter_dados_cliente(request.user)
    return render(request, 'dashboard_cliente.html', context)


@login_required
def atualizar_cliente_fragmento(request):
    context = obter_dados_cliente(request.user)
    return render(request, 'conteudo_cliente.html', context)


@login_required
def profile_redirect(request):
    """Redireciona o usuário logado para o dashboard apropriado.
    Médicos vão para `dashboard_medico`; outros para `dashboard_cliente`.
    """
    try:
        # se for médico, existe um Medico associado
        medico = Medico.objects.get(usuario=request.user)
        return redirect('dashboard_medico')
    except Medico.DoesNotExist:
        return redirect('dashboard_cliente')


def paciente_publico(request):
    """Página pública de demonstração do template do paciente (Tailwind)."""
    return render(request, 'paciente.html')


def agendar_paciente(request):
    if request.method != 'POST':
        return redirect('paciente_publico')

    nome = request.POST.get('nome') or 'Paciente'
    cpf = request.POST.get('cpf') or ''
    telefone = request.POST.get('telefone') or ''
    unidade = request.POST.get('unidade') or ''
    especialidade = request.POST.get('especialidade') or ''
    horario = request.POST.get('horario') or ''

    # escolher médico: por especialidade, senão primeiro
    medico = None
    try:
        if especialidade:
            medico = Medico.objects.filter(especialidade__icontains=especialidade).first()
        if not medico:
            medico = Medico.objects.first()
    except Exception:
        medico = None

    # gerar senha simples: S + total_hoje + 1
    hoje = timezone.now().date()
    cont = PacienteFila.objects.filter(horario_chegada__date=hoje).count() + 1
    senha = f"S{cont:03d}"

    if not medico:
        # sem médico disponível
        from django.urls import reverse
        return redirect(reverse('paciente_publico') + '?created=0')

    usuario = request.user if request.user.is_authenticated else None
    if usuario:
        nome = usuario.get_full_name() or usuario.username or nome

    paciente = PacienteFila.objects.create(
        usuario=usuario,
        nome=nome,
        cpf=cpf,
        senha=senha,
        medico_destinado=medico,
        status='aguardando',
        horario_chegada=timezone.now(),
    )

    # redirecionar com query param para exibir confirmação
    from django.urls import reverse
    params = f"?created=1&senha={senha}"
    return redirect(reverse('paciente_publico') + params)


def home(request):
    """Página inicial que liga todos os painéis e páginas relevantes."""
    # adicionar alguns dados rápidos para os cards da home
    try:
        total_membros = Membro.objects.count()
        ativos = Membro.objects.filter(status=True).count()
        medicos_count = Medico.objects.count()
        pacientes_aguardando = PacienteFila.objects.filter(status='aguardando').count()
        percentual_ativos = int((ativos / total_membros) * 100) if total_membros else 0
    except Exception:
        total_membros = ativos = medicos_count = pacientes_aguardando = percentual_ativos = 0

    context = {
        'total_membros': total_membros,
        'ativos': ativos,
        'medicos_count': medicos_count,
        'pacientes_aguardando': pacientes_aguardando,
        'percentual_ativos': percentual_ativos,
    }
    return render(request, 'home.html', context)




