from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserForm(forms.ModelForm):
    class Meta: #class used to change behavior of model fields
        model = User
        fields = ['name', 'email', 'password', 'telephone_number', 'company', 'active']

class SDGForm(forms.ModelForm):
    class Meta:
        model = SDG
        fields = ['sdg_number', 'title', 'description']

class MaterialityIssueForm(forms.ModelForm):
    class Meta:
        model = Materiality_Issue
        fields = ['materiality_issue_group', 'theme', 'criterion', 'description']

class StakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        fields = ['name', 'email', 'telephone_number', 'company']

class DemandForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = ['title', 'description']

class DemandReadOnlyForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = ['demand_id', 'insertion_date', 'title', 'description']
        widgets = {
            'demand_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'insertion_date': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class DemandAnalysisForm(forms.ModelForm):
    stakeholders = forms.ModelMultipleChoiceField(
        queryset=Stakeholder.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Stakeholders'
    )
    materiality_issues = forms.ModelMultipleChoiceField(
        queryset=Materiality_Issue.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Materiality Issues'
    )
    sdgs = forms.ModelMultipleChoiceField(
        queryset=SDG.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='SDGs'
    )

    class Meta:
        model = Demand
        fields = ['potential_impact_scale', 'potential_effort_scale', 'potential_beneficiaries', 'potential_beneficiaries_scale']
        widgets = {
            'potential_impact_scale': forms.Select(choices=[(i, i) for i in range(1, 5)]),
            'potential_effort_scale': forms.Select(choices=[(i, i) for i in range(1, 5)]),
        }

class Stakeholder_x_DemandForm(forms.ModelForm):
    class Meta:
        model = Stakeholder_x_Demands
        fields = ['stakeholder', 'demand']

class Demands_x_MaterialityForm(forms.ModelForm):
    class Meta:
        model = Demands_x_Materiality
        fields = ['materiality_issue', 'demand']

class SDG_x_DemandForm(forms.ModelForm):
    class Meta:
        model = SDG_x_Demands
        fields = ['sdg', 'demand']

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'description']


class ActionPlanForm(forms.ModelForm):
    class Meta:
        model = ActionPlan
        fields = ['title', 'responsible', 'start_date', 'end_date', 'scope_detail', 'estimated_cost']
