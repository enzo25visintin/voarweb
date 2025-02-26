from django.contrib import messages
from django.db.models.functions import Coalesce
from django.db.models import Avg, F, Value
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *
from datetime import date
from django.contrib.auth import login, logout


# Create your views here.

#Initial Views
def home(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated
    
    return render(request, 'ivw/home.html')

def about(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated
    
    return render(request, 'ivw/about.html')

#User Views
def user_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated 

    users = User.objects.all()
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(company__icontains=query) |
            models.Q(active__icontains=query) |
            models.Q(telephone_number__icontains=query) |
            models.Q(user_id__icontains=query)
        )
    return render(request, 'ivw/user_list.html', {'users': users})

def user_create(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'ivw/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])  # Hash new password
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'ivw/user_form.html', {'form': form})


#Login and Logout Views
def user_login(request):
    # Clear any previous messages before rendering the login page
    storage = messages.get_messages(request)
    storage.used = True  # This ensures old messages don't reappear

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.user_id  # Store session manually
                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to homepage or dashboard
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, "ivw/login.html")

def user_logout(request):
    # Clear any previous messages before rendering the login page
    storage = messages.get_messages(request)
    storage.used = True  # This ensures old messages don't reappear

    request.session.flush()  # Clears the session
    messages.success(request, "You have been logged out.")
    return redirect("login")


#SDGs
def sdg_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated 

    sdgs = SDG.objects.all()
    query = request.GET.get('q')
    if query:
        sdgs = SDG.objects.filter(
            models.Q(sdg_number__icontains=query) |
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query) 
        )
    return render(request, 'ivw/sdg_list.html', {'sdgs': sdgs})

def sdg_create(request):
    if request.method == 'POST':
        form = SDGForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sdg_list')
    else:
        form = SDGForm()
    return render(request, 'ivw/sdg_form.html', {'form': form})

def sdg_update(request, pk):
    sdg = get_object_or_404(SDG, pk=pk)
    if request.method == 'POST':
        form = SDGForm(request.POST, instance=sdg)
        if form.is_valid():
            form.save()
            return redirect('sdg_list')
    else:
        form = SDGForm(instance=sdg)
    return render(request, 'ivw/sdg_form.html', {'form': form})


#Materiality
def materiality_issue_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated 

    issues = Materiality_Issue.objects.all()
    query = request.GET.get('q')
    if query:
        issues = Materiality_Issue.objects.filter(
            models.Q(materiality_issue_id__icontains=query) |
            models.Q(materiality_issue_group__icontains=query) |
            models.Q(theme__icontains=query) |
            models.Q(criterion__icontains=query) |
            models.Q(description__icontains=query) 
        )
    return render(request, 'ivw/materiality_issue_list.html', {'issues': issues})

def materiality_issue_create(request):
    if request.method == 'POST':
        form = MaterialityIssueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materiality_issue_list')
    else:
        form = MaterialityIssueForm()
    return render(request, 'ivw/materiality_issue_form.html', {'form': form})

def materiality_issue_update(request, pk):
    issue = get_object_or_404(Materiality_Issue, pk=pk)
    if request.method == 'POST':
        form = MaterialityIssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            return redirect('materiality_issue_list')
    else:
        form = MaterialityIssueForm(instance=issue)
    return render(request, 'ivw/materiality_issue_form.html', {'form': form})


#Stakeholders
def stakeholder_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated

    stakeholders = Stakeholder.objects.all()
    query = request.GET.get('q')
    if query:
        stakeholders = Stakeholder.objects.filter(
            models.Q(stakeholder_id__icontains=query) |
            models.Q(name__icontains=query) |
            models.Q(email__icontains=query) |
            models.Q(telephone_number__icontains=query) |
            models.Q(company__icontains=query) 
        )
    return render(request, 'ivw/stakeholder_list.html', {'stakeholders': stakeholders})

def stakeholder_create(request):
    if request.method == 'POST':
        form = StakeholderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stakeholder_list')
    else:
        form = StakeholderForm()
    return render(request, 'ivw/stakeholder_form.html', {'form': form})

def stakeholder_update(request, pk):
    stakeholder = get_object_or_404(Stakeholder, pk=pk)
    if request.method == 'POST':
        form = StakeholderForm(request.POST, instance=stakeholder)
        if form.is_valid():
            form.save()
            return redirect('stakeholder_list')
    else:
        form = StakeholderForm(instance=stakeholder)
    return render(request, 'ivw/stakeholder_form.html', {'form': form})

#Demands
def demand_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated

    demands = Demand.objects.all()
    query = request.GET.get('q')
    if query:
        demands = Demand.objects.filter(
            models.Q(status__icontains=query) |
            models.Q(insertion_date__icontains=query) |
            models.Q(title__icontains=query) |
            models.Q(demand_id__icontains=query) |
            models.Q(description__icontains=query)
        )

    return render(request, 'ivw/demand_list.html', {'demands': demands})

def demand_create(request):
    if request.method == 'POST':
        form = DemandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demand_list')
    else:
        form = DemandForm()
    return render(request, 'ivw/demand_form.html', {'form': form})

def demand_update(request, pk):
    demand = get_object_or_404(Demand, pk=pk)
    if request.method == 'POST':
        form = DemandForm(request.POST, instance=demand)
        if form.is_valid():
            form.save()
            return redirect('demand_list')
    else:
        form = DemandReadOnlyForm(instance=demand)
    return render(request, 'ivw/demand_form.html', {'form': form})

#Demand Analysis i
def demand_analysis_i(request, pk):
    demand = get_object_or_404(Demand, pk=pk)
    stakeholders = Stakeholder.objects.all()
    materiality_issues = Materiality_Issue.objects.all()
    sdgs = SDG.objects.all()

    # Recuperar os itens já associados à demanda
    selected_stakeholders = Stakeholder.objects.filter(stakeholder_x_demands__demand=demand)
    selected_materiality_issues = Materiality_Issue.objects.filter(demands_x_materiality__demand=demand)
    selected_sdgs = SDG.objects.filter(sdg_x_demands__demand=demand)


    if request.method == 'POST':
        form = DemandAnalysisForm(request.POST)
        if form.is_valid():
            stakeholders_selected = form.cleaned_data['stakeholders']
            materiality_issues_selected = form.cleaned_data['materiality_issues']
            sdgs_selected = form.cleaned_data['sdgs']
            
            # Processar os stakeholders selecionados
            Stakeholder_x_Demands.objects.filter(demand=demand).delete()
            for stakeholder in stakeholders_selected:
                Stakeholder_x_Demands.objects.get_or_create(stakeholder=stakeholder, demand=demand)
            
            # Processar os materiality issues selecionados
            Demands_x_Materiality.objects.filter(demand=demand).delete()
            for materiality in materiality_issues_selected:
                Demands_x_Materiality.objects.get_or_create(materiality_issue=materiality, demand=demand)
            
            # Processar os SDGs selecionados
            SDG_x_Demands.objects.filter(demand=demand).delete()
            for sdg in sdgs_selected:
                SDG_x_Demands.objects.get_or_create(sdg=sdg, demand=demand)
            
            return redirect('demand_analysis_ii', pk=demand.pk)
        else:
            stakeholders_selected = form.cleaned_data.get('stakeholders', selected_stakeholders)
            materiality_issues_selected = form.cleaned_data.get('materiality_issues', selected_materiality_issues)
            sdgs_selected = form.cleaned_data.get('sdgs', selected_sdgs)
    else:
        form = DemandAnalysisForm(initial={
            'stakeholders': selected_stakeholders,
            'materiality_issues': selected_materiality_issues,
            'sdgs': selected_sdgs,
        })

        return render(request, 'ivw/demand_analysis_i.html', {
            'form': form,
            'stakeholders': stakeholders,
            'materiality_issues': materiality_issues,
            'sdgs': sdgs,
            'demand': demand
        })

        
        
        #return render(request, 'ivw/demand_analysis_i.html', {'stakeholders': stakeholders, 'materiality_issues': materiality_issues, 'sdgs': sdgs, 'demand': demand})

#Demand analysis ii
def demand_analysis_ii(request, pk):
    demand = get_object_or_404(Demand, pk=pk)
    stakeholders = Stakeholder.objects.filter(stakeholder_x_demands__demand=demand)
    materiality_issues = Materiality_Issue.objects.filter(demands_x_materiality__demand=demand)
    sdgs = SDG.objects.filter(sdg_x_demands__demand=demand)


    if request.method == 'POST':
        form = DemandAnalysisForm(request.POST, instance=demand)
        if form.is_valid():
            demand = form.save(commit=False)  # Capture os dados do formulário sem salvar no banco de dados ainda
            demand.status = 'Aguardando Priorização'  # Atualize o campo status
            demand.save()  # Salve os dados no banco de dados

            #form.save()
            # Adicionar uma mensagem de sucesso
            messages.success(request, 'Dados gravados com sucesso!')
            return redirect('demand_list')
        else:
            messages.error(request, 'Erro ao gravar os dados. Verifique o formulário e tente novamente.')
            print(form.errors)

    else:
        form = DemandAnalysisForm(instance=demand)

    return render(request, 'ivw/demand_analysis_ii.html', {
        'demand': demand,
        'stakeholders': stakeholders,
        'materiality_issues': materiality_issues,
        'sdgs': sdgs,
        'form': form
    })

#Programs
def program_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated

    programs = Program.objects.all()
    query = request.GET.get('q')
    if query:
        programs = Program.objects.filter(
            models.Q(program_id__icontains=query) |
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)  
        )
    return render(request, 'ivw/program_list.html', {'programs': programs})

def program_create(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'ivw/program_form.html', {'form': form})

def program_update(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'ivw/program_form.html', {'form': form})

#Demand authorization
def demand_funnel(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated

    # Recuperar todas as demandas com status "Aguardando Priorização"
    demands = Demand.objects.filter(status='Aguardando Priorização').annotate(
        significancy=(F('potential_impact_scale') + F('potential_effort_scale') + F('potential_beneficiaries_scale')) / 3
    ).order_by('-significancy')
    query = request.GET.get('q')
    if query:
        demands = Demand.objects.filter(
            models.Q(demand_id__icontains=query) |
            models.Q(title__icontains=query) |
            models.Q(potential_impact_scale__icontains=query) |
            models.Q(potential_effort_scale__icontains=query) |
            models.Q(potential_beneficiaries__icontains=query) |
            models.Q(potential_beneficiaries_scale__icontains=query) |
            models.Q(status__icontains=query) 
        )

    # Copiar o status de cada demanda para a tabela temporária
    for demand in demands:
        aux_status, created = TemporaryDemandStatus.objects.get_or_create(demand=demand)
        aux_status.status = demand.status
        aux_status.save()

    # Preparar os dados para renderização
    demand_list = []
    for demand in demands:
        aux_status = TemporaryDemandStatus.objects.get(demand=demand)
        demand_list.append({
            'demand_id': demand.demand_id,
            'title': demand.title,
            'potential_impact_scale': demand.potential_impact_scale,
            'potential_effort_scale': demand.potential_effort_scale,
            'potential_beneficiaries_scale': demand.potential_beneficiaries_scale,
            'significancy': demand.significancy,
            'potential_beneficiaries': demand.potential_beneficiaries,
            'status': aux_status.status,
            'pk': demand.pk
        })

    return render(request, 'ivw/demand_funnel.html', {
        'demands': demand_list
    })


def save_changes(request):
    if request.method == 'POST':
        demands = Demand.objects.filter(status='Aguardando Priorização').annotate(
            significancy=(F('potential_impact_scale') + F('potential_effort_scale') + F('potential_beneficiaries_scale')) / 3
        ).order_by('-significancy')

        for demand in demands:
            status = request.POST.get(f'status_{demand.pk}')
            aux_status, created = TemporaryDemandStatus.objects.get_or_create(demand=demand)
            aux_status.status = status
            aux_status.save()

        if 'detail' in request.POST:
            demand_id = request.POST['detail']
            return redirect('demand_detail', pk=demand_id)
        return redirect('demand_funnel')


def demand_detail(request, pk):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated

    demand = get_object_or_404(Demand, pk=pk)
    return render(request, 'ivw/demand_details.html', {'demand': demand})

def conclude_funnel(request):
    if request.method == 'POST':
        return render(request, 'ivw/conclude_funnel.html')
    else:
        return redirect('demand_funnel')

def finalize_funnel(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            aux_statuses = TemporaryDemandStatus.objects.all()
            for aux_status in aux_statuses:
                demand = aux_status.demand
                demand.status = aux_status.status
                demand.analysis_date = date.today()
                demand.save()
            TemporaryDemandStatus.objects.all().delete()
        elif 'cancel' in request.POST:
            # Apenas retorna ao funil sem salvar
            return redirect('demand_funnel')
        elif 'abandon' in request.POST:
            # Apaga todos os registros temporários e retorna para a home
            TemporaryDemandStatus.objects.all().delete()
            return redirect('home')

    return redirect('demand_funnel')

def update_status(request):
    if request.method == 'POST':
        demand_id = request.POST.get('demand_id')
        new_status = request.POST.get('new_status')
        
        print('Received Demand ID:', demand_id)  # Verifique se o demand_id está correto
        print('Received New Status:', new_status)  # Verifique se o new_status está correto
        
        try:
            demand = Demand.objects.get(demand_id=demand_id)
            aux_status, created = TemporaryDemandStatus.objects.get_or_create(demand=demand)
            aux_status.status = new_status
            aux_status.save()
            return JsonResponse({'success': True})
        except Demand.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Demand not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

#Planning of demands
def planning_list(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated
    
    demands = Demand.objects.filter(status='Aprovada')
    query = request.GET.get('q')
    if query:
        demands = Demand.objects.filter(
            models.Q(demand_id__icontains=query) |
            models.Q(title__icontains=query) |
            models.Q(status__icontains=query) 
        )
    return render(request, 'ivw/planning_list.html', {'demands': demands})


def planning_demand_detail(request, demand_id):
    demand = get_object_or_404(Demand, pk=demand_id)
    stakeholders = Stakeholder.objects.filter(stakeholder_x_demands__demand_id=demand_id)
    materiality_issues = Materiality_Issue.objects.filter(demands_x_materiality__demand_id=demand_id)
    sdgs = SDG.objects.filter(sdg_x_demands__demand_id=demand_id)
    return render(request, 'ivw/planning_demand_detail.html', {
        'demand': demand,
        'stakeholders': stakeholders,
        'materiality_issues': materiality_issues,
        'sdgs': sdgs
    })


def action_plan_list(request, demand_id):
    demand = get_object_or_404(Demand, pk=demand_id)
    action_plans = demand.action_plans.all()
    query = request.GET.get('q')
    if query:
        action_plans = ActionPlan.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(responsible__icontains=query) |
            models.Q(start_date__icontains=query) |
            models.Q(end_date__icontains=query) |
            models.Q(estimated_cost__icontains=query) 
        )
    return render(request, 'ivw/action_plan_list.html', {'demand': demand, 'action_plans': action_plans})

def action_plan_create(request, demand_id):
    demand = get_object_or_404(Demand, pk=demand_id)
    if request.method == 'POST':
        form = ActionPlanForm(request.POST)
        if form.is_valid():
            action_plan = form.save(commit=False)
            action_plan.demand = demand
            action_plan.save()
            return redirect('action_plan_list', demand_id=demand_id)
    else:
        form = ActionPlanForm()
    return render(request, 'ivw/action_plan_form.html', {'form': form, 'demand': demand})

def action_plan_update(request, demand_id, pk):
    demand = get_object_or_404(Demand, pk=demand_id)
    action_plan = get_object_or_404(ActionPlan, pk=pk)
    if request.method == 'POST':
        form = ActionPlanForm(request.POST, instance=action_plan)
        if form.is_valid():
            form.save()
            return redirect('action_plan_list', demand_id=demand_id)
    else:
        form = ActionPlanForm(instance=action_plan)
    return render(request, 'ivw/action_plan_form.html', {'form': form, 'demand': demand})


def finalize_planning(request, demand_id):
    demand = get_object_or_404(Demand, pk=demand_id)
    action_plans = demand.action_plans.all()
    #for action_plan in action_plans:
    #    action_plan.status = 'Em Execução'
    #    action_plan.save()
    #demand.status = 'Em Execução'
    #demand.save()
    return redirect('planning_list')


def complete_prioritization(request):
    #This page requires authentication
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login page if not authenticated

    # Atualizar o status de todas as demandas aprovadas e seus planos de ação para "Em Execução"
    approved_demands = Demand.objects.filter(status='Aprovada')
    for demand in approved_demands:
        demand.status = 'Em Execução'
        demand.save()
        action_plans = demand.action_plans.all()
        for action_plan in action_plans:
            action_plan.status = 'Em Execução'
            action_plan.save()
    return redirect('home')


