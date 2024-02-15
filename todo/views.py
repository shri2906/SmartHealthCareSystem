from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .symptoms_list import *
from .models import User_info
from PIL import ImageFont, ImageDraw, Image  
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile, File
from django.http import HttpResponse
import os
from .CNN_TESTING import get_result


def home(request):
    return render(request, 'todo/home.html')

class convert_to_class:
    def __init__(self,a,b):
        self.user_identity = a
        self.user_id_to_search = b


@login_required
def check_detail(request):
    if request.method == 'GET':
        user_info = User_info.objects.all()
        user_identity = []
        user_id_to_search = []

        for u in user_info:
            if u.role == "User":
                user_identity.append(u.first_name + " " + u.last_name + " {" + str(User.objects.all().filter(id = u.user_id)[0]) + "}")
                user_id_to_search.append(User.objects.all().filter(id = u.user_id)[0].id)
        print(user_id_to_search)
        print(user_identity)

        data_information = []
        for i in range(len(user_id_to_search)):
            data_information.append(convert_to_class(user_identity[i],user_id_to_search[i]))

        return render(request, 'todo/check_detail.html',{'data_information':data_information})

    else:
        patient_id = request.POST['patient']
        print(patient_id)
        user_info = User_info.objects.all().filter(user_id = int(patient_id))
        disease_info = Todo.objects.all().filter(user_id = int(patient_id))
        return render(request, 'todo/check_detail.html',{'user_info':user_info,'disease_info':disease_info})


@login_required
def your_profile(request):

    user_info = User_info.objects.all().filter(user_id = request.user.id)
    user_adhar_num = User.objects.all().filter(id = request.user.id)[0]
    
    if request.method == 'GET':
        return render(request, 'todo/your_profile.html',{'user_info':user_info})
    else:
        print(user_info[0].first_name)
        print(User.username)
        image = Image.open("HEALTH_CARD.png")  
        draw = ImageDraw.Draw(image)  
        font = ImageFont.truetype("arial.ttf", 15)  
        draw.text((10, 250), "Name: " + user_info[0].first_name + " "  + user_info[0].last_name , font=font, fill='#000000')  
        draw.text((10, 280), "Adress: " + user_info[0].Address, font=font, fill='#000000')  
        draw.text((10, 310), "Date of Birth: " + str(user_info[0].dob), font=font, fill='#000000')  
        draw.text((10, 340), "Mobile: " + user_info[0].mobile, font=font, fill='#000000')  
        draw.text((10, 370), "Email: " + user_info[0].Email_ID, font=font, fill='#000000')  
        draw.text((10, 400), "Health Insurance Number : " + user_info[0].hin, font=font, fill='#000000')  
        draw.text((10, 430), "Adhar Card number : " + str(user_adhar_num), font=font, fill='#000000')  
        image = image.convert('RGB')
        path = "todo/Health_Card.pdf"
        image.save(path)
        if os.path.exists(path):
            with open(path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
                return response

        return render(request, 'todo/your_profile.html',{'user_info':user_info})



def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['adhar_num'], password=request.POST['password1'])
                user.save()
                user_info = User_info()
                user_info.user = user
                user_info.first_name = request.POST['first_name']
                user_info.last_name = request.POST['last_name']
                user_info.dob = request.POST['dob']
                user_info.gender = request.POST['gender']
                user_info.mobile = request.POST['Mobile_Number']
                user_info.Email_ID = request.POST['Email_ID']
                user_info.Address = request.POST['Address']
                user_info.hin = request.POST['hin']
                user_info.role = "User"
                user_info.save()            

                login(request, user)

                return render(request, 'todo/home.html')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That adhar card number has already been taken. Please check your adhar card number carefully'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


def doctor_signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/doctor_signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['adhar_num'], password=request.POST['password1'],is_staff=True)
                user.save()

                user_info = User_info()
                user_info.user = user
                user_info.first_name = request.POST['first_name']
                user_info.last_name = request.POST['last_name']
                user_info.dob = request.POST['dob']
                user_info.gender = request.POST['gender']
                user_info.mobile = request.POST['Mobile_Number']
                user_info.Email_ID = request.POST['Email_ID']
                user_info.Address = request.POST['Address']
                user_info.hin = request.POST['hin']
                user_info.role = "Doctor"
                user_info.save()            

                login(request, user)

                return render(request, 'todo/home.html')
            except IntegrityError:
                return render(request, 'todo/doctor_signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'todo/doctor_signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})




def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})



@login_required
def predict_disease(request):
        return render(request, 'todo/predict_disease.html', {'form':TodoForm(),'symptoms':symptoms})


@login_required
def predicted_results(request):
    if request.method == 'GET':
        sym1 =request.GET['sys1']
        sym2 =request.GET['sys2']
        sym3 =request.GET['sys3']
        sym4 =request.GET['sys4']
        sym5 =request.GET['sys5']
        
        syms = [sym1,sym2,sym3,sym4,sym5]
        symptoms = []
        for sym in syms:
            if sym != 'none':
                symptoms.append(sym.replace('_',' '))
                
        symptoms_inserted = syms
        result,acc,doctor_info,exercise_info,diet_info,medicine_info = get_result(symptoms_inserted)
        print(result)
 
        return render(request, 'todo/predicted_result.html',{'form':TodoForm(),'symptoms':symptoms,'disease':result,'doctor':doctor_info,'excersize':exercise_info, 'accuracy':acc,'diet':diet_info ,'medicine':medicine_info})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
