from parachapp.models import Student,User,Attend,Teacher
from django.shortcuts import redirect, render
from django.urls import reverse
from parachapp.forms import StudentSignUpForm, TeacherSignUpForm, StudentUpdateForm,StudentAccountChangeUpdate,AttendanceForm,NotificationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Count, Min


import datetime
from datetime import date, timedelta


def index(request):
    return render(request, 'parachapp/index.html')



def student_home(request):
    student = Student.objects.order_by('-user_id')[:9]
    context = {
        'student':student
    }
    return render(request, 'parachapp/student_home.html', context)

def teacher_home(request):
    teacher = Teacher.objects.order_by('-user_id')[:9]

    context = {
        'teacher':teacher
    }

    return render(request, 'parachapp/teacher_home.html', context)


def student_sign_up(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parachapp:login')
    else:
        form = StudentSignUpForm()
    return render(request, 'parachapp/student_reg.html', {'form':form})

def success_account(request):
    student= Student.objects.all()
    
    return render(request, 'parachapp/success_account.html', {'student':student})

def teacher_sign_up(request):
    if request.method == 'POST':
        teacher_reg_form = TeacherSignUpForm(request.POST)
        if teacher_reg_form.is_valid():
            teacher_reg_form.save()
            return redirect('parachapp:login')
    else:
        teacher_reg_form = TeacherSignUpForm()
    return render(request, 'parachapp/teacher_reg.html', {'teacher_reg_form':teacher_reg_form})

def login_request(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user != None:
                login(request, user)
                if user.is_student == True:
                    return redirect(reverse('parachapp:student_updates', kwargs={'pk':request.user.pk}))
                elif user.is_teacher == True:
                    return redirect('parachapp:teacher_home')
                elif user.is_superuser:
                    return redirect('parachapp:student_home')
            else:
                messages.error(request, "Invalid Login Credentials!")
                #return HttpResponseRedirect("/")
                return redirect('parachapp:login')
    else:
        login_form = AuthenticationForm()
    return render(request, 'parachapp/login.html', {'login_form':login_form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")
