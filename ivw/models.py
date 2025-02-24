from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    Active_choices = [('A', 'Active'), ('I','Inactive'),]
    
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    telephone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=100)
    active = models.CharField(max_length=1, choices=Active_choices, default='1')


    def __str__(self):
        return self.name


class SDG(models.Model):
    sdg_number = models.PositiveSmallIntegerField(primary_key=True)  # Number of two characters
    title = models.CharField(max_length=200) 
    description = models.TextField(max_length=3000) 

    def __str__(self):
        return f"{self.sdg_number} - {self.title}"


class Materiality_Issue(models.Model):
    materiality_issue_id = models.AutoField(primary_key=True)
    materiality_issue_group = models.CharField(max_length=200)
    theme = models.CharField(max_length=200)
    criterion = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.materiality_issue_group} - {self.theme} - {self.criterion}"


class Stakeholder(models.Model):
    stakeholder_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    telephone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Demand(models.Model):
    demand_id = models.AutoField(primary_key=True)
    insertion_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    description = models.TextField()

    potential_impact_scale = models.PositiveSmallIntegerField(null=True, blank=True)
    potential_effort_scale = models.PositiveSmallIntegerField(null=True, blank=True)
    potential_beneficiaries = models.PositiveIntegerField(null=True, blank=True)
    potential_beneficiaries_scale = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Aguardando Priorização")

    def __str__(self):
        return self.title

class Stakeholder_x_Demands(models.Model):
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)

class Demands_x_Materiality(models.Model):
    materiality_issue = models.ForeignKey(Materiality_Issue, on_delete=models.CASCADE)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)

class SDG_x_Demands(models.Model):
    sdg = models.ForeignKey(SDG, on_delete=models.CASCADE)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
