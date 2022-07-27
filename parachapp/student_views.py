from parachapp.models import Student,User,Attend,StudentAdvancedProfile,UploadFile
from django.shortcuts import redirect, render
from django.urls import reverse
from parachapp.forms import StudentSignUpForm, TeacherSignUpForm, StudentUpdateForm,StudentAccountChangeUpdate,AttendanceForm,NotificationForm,StudentAdvancedProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Count, Min
from django.core.files.storage import FileSystemStorage #To upload Profile Picture

import datetime
from datetime import date, timedelta

def student_detail(request,pk):
    uploadfile = UploadFile.objects.all()
    student = Student.objects.get(pk=pk)
    student_ids = Student.objects.get(pk=pk)
    sinstance = StudentAdvancedProfile.objects.get(studentinstance=student_ids)
    instanceprofile = sinstance.studentinstance.studentadvancedprofile_set.all()

    vv=Attend.objects.filter(attender=student_ids)
    
    #payment calculations
    #balance = student.course.price - student.amountpaid
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        attender_id = Attend()
        

        if form.is_valid():
            date_present = form.cleaned_data['date_present']
            attender_id.date_present = date_present
            attender_id.attender = student_ids
            

            if date_present != date.today():
                print('============it must be todays date')
                messages.error(request, 'sorry! you can only mark attendance for todays date')
                return redirect('.')
                
            unique_fields = ['attender_id', 'date_present']
            duplicates = (
                Attend.objects.values(*unique_fields)
                .order_by()
                .annotate(max_id=Min('id'), count_id=Count('id'))
                .filter(count_id__gt=1)
            )
            for duplicate in duplicates:
                (
                    Attend.objects
                    .filter(**{x: duplicate[x] for x in unique_fields})
                    .exclude(id=duplicate['max_id'])
                    .delete()
                )
                messages.error(request, 'sorry, attendance has been marked for today, you cannot mark twice')
                return redirect('.')
            attender_id.save()
            messages.success(request, 'attendance has been marked successfully!')
            return redirect('.')
    else:
        form = AttendanceForm()
        

    context = {
        'student':student,
        'student_ids':student_ids,
        'form':form,
        'vv':vv,
        'instanceprofile':instanceprofile,
        'uploadfile':uploadfile
    }
 
    return render(request, 'student_template/student_detail.html', context)

def student_update(request,pk):

    user_id = User.objects.get(pk=pk)
    student_id = Student.objects.get(pk=pk)
    if request.method == 'POST':
        s_update_form = StudentAccountChangeUpdate(request.POST, instance = user_id)
        sudent_update_form = StudentUpdateForm(request.POST, request.FILES, instance=student_id)
        print('==============', user_id)
        if sudent_update_form.is_valid() and s_update_form.is_valid():
            print('=============== valid')
            s_update_form.save()
            #print(sudent_update_form, '==============')
            sudent_update_form.save()
            
            #return redirect('customuserapp:student_details', pk=pk)
            return redirect(reverse('parachapp:student_details', kwargs={'pk':pk}))
    else:
        s_update_form = StudentAccountChangeUpdate(instance = user_id)
        sudent_update_form = StudentUpdateForm(instance=student_id)
        

    context = {
        's_update_form':s_update_form,
        'sudent_update_form':sudent_update_form
        
    }

    return render(request, 'student_template/student_update.html',context)


#this is an update view for the admin
def student_advanced_update(request,pk):
    student_id = Student.objects.get(pk=pk)
    sinstance = StudentAdvancedProfile.objects.get(studentinstance=student_id)
    if request.method == 'POST':
        advanced_update_form = StudentAdvancedProfileForm(request.POST, instance = sinstance)
        
        if advanced_update_form.is_valid():
            advanced_update_form.save()
            
            #return redirect('customuserapp:student_details', pk=pk)
            return redirect(reverse('parachapp:student_details', kwargs={'pk':pk}))
    else:
        advanced_update_form = StudentAdvancedProfileForm(instance=sinstance)

    context = {
        'advanced_update_form':advanced_update_form,
    }

    return render(request, 'student_template/student_advanced_update.html',context)

#delete view for students
def student_delete(request,pk):
    student = Student.objects.get(pk=pk)
    student_delete_form = Student.objects.get(pk=pk)
    if request.method == 'POST':
        student_delete_form.delete()
        return redirect('parachapp:student_home')
    context = {
        'student_delete_form':student_delete_form,
        'student':student
    }

    return render(request, 'student_template/student_delete.html',context)

def att_detail(request,pk):
    
    attendance_days = Attend.objects.get(pk=pk)
    
    return render(request, 'student_template/att_detail.html', {'attendance_days':attendance_days})    
