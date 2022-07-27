from decimal import Context
from parachapp.models import Course, Student, Teacher,User,Attend,StudentAdvancedProfile,Salary
from django.shortcuts import redirect, render
from django.urls import reverse
from parachapp.forms import (StudentSignUpForm, TeacherSignUpForm, 
                                StudentUpdateForm,StudentAccountChangeUpdate,
                                AttendanceForm,NotificationForm,
                                CreateStudySessionForm,CreateCourseForm,UpdateCourseForm,
                                UpdateSalaryForm,
                                UploadFile,
                                UploadFileForm,
                                )
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Count, Min


import datetime
from datetime import date, timedelta


def adminhome(request):
    
    course = Course.objects.all()
    student = Student.objects.all()
    student_count = Student.objects.all().count()
    teacher_count = Teacher.objects.all().count()

    advanced_profile_instance = StudentAdvancedProfile.objects.all()
    pending_payments = StudentAdvancedProfile.objects.filter(payment_status='Not Fully Paid').count()
    completed_payments = StudentAdvancedProfile.objects.filter(payment_status='Fully Paid').count()
    

    context ={
        'student':student,
        'student_count':student_count,
        'pending_payments':pending_payments,
        'completed_payments':completed_payments,
        'advanced_profile_instance':advanced_profile_instance,
        'course':course,
        'teacher_count':teacher_count
    }
    return render(request, 'admin_template/admin-home.html', context)

def payment_stat(request):
    
    studentavancedprofile = StudentAdvancedProfile.objects.all()
    
    context ={
        'studentavancedprofile':studentavancedprofile
    }
    return render(request, 'admin_template/payment_stat.html', context)

def create_course(request):
    course = Course.objects.all()
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course has been created successfully')
            return redirect('.')
    else:
        form = CreateCourseForm()

    context = {
        'form':form,
        'course':course
    }
    
    return render(request, 'admin_template/add_course.html',context)

def update_course(request,pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course has been updated successfully')
            return redirect('parachapp:create_course')
    else:
        form = UpdateCourseForm(instance=course)

    context = {
        'form':form,
        
    }
    
    return render(request, 'admin_template/update_course.html',context)

def delete_course(request,pk):
    form = Course.objects.get(pk=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('parachapp:create_course')
    context = {
        'form':form,
        
    }
    return render(request, 'admin_template/delete_course.html',context)

def create_teacher(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'account has been created for teacher proceed to update')
            return redirect('parachapp:teacher_home')
    else:
        form = TeacherSignUpForm()
    
    return render(request, 'admin_template/createteacher.html',{'form':form,})

def create_student(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'account has been created for student proceed to update')
            return redirect('parachapp:student_home')
    else:
        form = StudentSignUpForm()
    
    return render(request, 'admin_template/createstudent.html',{'form':form,})

def fileupload(request):
    uploadfile = UploadFile.objects.all()
    if request.method == 'POST':
        uploadfileform = UploadFileForm(request.POST, request.FILES)
        
        if uploadfileform.is_valid():
            print('=========== yes')
            uploadfileform.save()
            
            return redirect('.')
    else:
        uploadfileform = UploadFileForm()
    
    context = {
        'uploadfile':uploadfile,
        'uploadfileform':uploadfileform
    }

    return render(request, 'admin_template/file_home.html',context)

def download(request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/files')
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise Http404

def liveclass(request):
    
    return render(request, 'admin_template/live-classes.html')

def notifications(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parachapp:student_home')
    else:
        form = NotificationForm()
    return render(request, 'admin_template/notify.html', {'form':form})

def salaryhome(request):
    salary = Salary.objects.all()

    context = {
        'salary':salary
    }
    return render(request, 'admin_template/salary.html', context)



def update_salary(request,pk):
    salary = Salary.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateSalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
            messages.success(request, 'salary has been updated successfully')
            return redirect('parachapp:salaryhome')
    else:
        form = UpdateSalaryForm(instance=salary)

    context = {
        'form':form,
    }
    
    return render(request, 'admin_template/salary_update.html',context)

def delete_salary(request,pk):
    form = Salary.objects.get(pk=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('parachapp:salaryhome')
    context = {
        'form':form,
        
    }
    return render(request, 'admin_template/delete_salary.html',context)