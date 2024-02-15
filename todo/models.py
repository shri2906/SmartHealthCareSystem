from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    medicine = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  str(self.user) + " {" + self.title + " } " +  str(self.datecompleted)




class User_info(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_name')
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    dob = models.DateField()
    gender = models.CharField(max_length=40)
    mobile = models.CharField(max_length=40)
    Email_ID = models.CharField(max_length=40)
    Address = models.CharField(max_length=40)
    hin = models.CharField(max_length=40)# health insurance number
    role = models.CharField(max_length=40)
    def __str__(self):
        return self.user.username

        # if self.verified == False:
        #     return self.user.username + " {" + self.Proprietor_name + "} : [Not verified yet]" 
        # else:
        #     return self.user.username + " {" + self.Proprietor_name + "}"

