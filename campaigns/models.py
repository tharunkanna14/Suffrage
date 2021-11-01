from django.db import models

from users.models import CustomUser
 
# Create your models here.
 
class Campaign(models.Model):
    organization_name = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
 
    def __str__(self):
        return self.organization_name
 
 
class Candidates(models.Model):
    organization_name = models.ForeignKey(Campaign, on_delete = models.CASCADE)
    candidate_list = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)

 
    def __str__(self):
        return self.candidate_list
    
    class meta:
        verbose_name = "Candidate"
