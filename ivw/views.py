from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *

# Create your views here.


def home(request):
    return render(request, 'ivw/home.html')

def about(request):
    return render(request, 'ivw/about.html')


#Users
def user_list(request):
    users = User.objects.all()
    return render(request, 'ivw/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'ivw/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'ivw/user_form.html', {'form': form})


#SDGs
def sdg_list(request):
    sdgs = SDG.objects.all()
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
    issues = Materiality_Issue.objects.all()
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
    stakeholders = Stakeholder.objects.all()
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
    demands = Demand.objects.all()
    query = request.GET.get('q')
    if query:
        demands = Demand.objects.filter(
            models.Q(status__icontains=query) |
            models.Q(insertion_date__icontains=query) |
            models.Q(title__icontains=query) |
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
        return render(request, 'ivw/demand_analysis_i.html', {'stakeholders': stakeholders, 'materiality_issues': materiality_issues, 'sdgs': sdgs, 'demand': demand})


def demand_analysis_ii(request, pk):
    demand = get_object_or_404(Demand, pk=pk)
    if request.method == 'POST':
        form = DemandAnalysisForm(request.POST, instance=demand)
        if form.is_valid():
            demand.status = "Aguardando Priorização"
            form.save()
            return redirect('demand_list')
    else:
        form = DemandAnalysisForm(instance=demand)
    return render(request, 'ivw/demand_analysis_ii.html', {'demand': demand, 'form': form})

