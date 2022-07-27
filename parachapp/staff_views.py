from parachapp.models import Salary, Student,Teacher,User,Attend,StudentAdvancedProfile
from django.shortcuts import redirect, render
from django.urls import reverse
from parachapp.forms import (StudentSignUpForm, TeacherSignUpForm, 
                                TeacherUpdateForm,TeacherAccountChangeUpdate,AttendanceForm,
                                NotificationForm,StudentAdvancedProfileForm,
                                PaySalaryForm
                            )
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from django.db.models import Count, Min
from django.core.files.storage import FileSystemStorage #To upload Profile Picture

def teacher_detail(request,pk):
    teacher = Teacher.objects.get(pk=pk)
    salaryinstance=Salary.objects.filter(teacherinstance=teacher)

    if request.method == 'POST':
        form = PaySalaryForm(request.POST)
        teachersalaryid = Salary()
        if form.is_valid():
            amount = form.cleaned_data['amount']
            teachersalaryid.amount = amount
            teachersalaryid.teacherinstance = teacher
            
            teachersalaryid.save()
            messages.success(request, 'attendance has been marked successfully!')
            return redirect('.')
    else:
        form = PaySalaryForm()
   
    context = {
      'teacher':teacher,
      'salaryinstance':salaryinstance,
      'form':form,
    }
 
    return render(request, 'staff_template/teacher_detail.html', context)


def teacher_update(request,pk):

    user_id = User.objects.get(pk=pk)
    teacher_id = Teacher.objects.get(pk=pk)
    if request.method == 'POST':
        t_update_form = TeacherAccountChangeUpdate(request.POST, instance = user_id)
        teacher_update_form = TeacherUpdateForm(request.POST, request.FILES, instance=teacher_id)
        print('==============', user_id)
        if t_update_form.is_valid() and teacher_update_form.is_valid():
            print('=========valid')
            t_update_form.save()
            teacher_update_form.save()
            
            #return redirect('customuserapp:student_details', pk=pk)
            return redirect(reverse('parachapp:teacher_details', kwargs={'pk':pk}))
    else:
        t_update_form = TeacherAccountChangeUpdate(instance = user_id)
        teacher_update_form = TeacherUpdateForm(instance=teacher_id)
        

    context = {
        't_update_form':t_update_form,
        'teacher_update_form':teacher_update_form
        
    }

    return render(request, 'staff_template/teacher_update.html',context)

#delete view for students
def teacher_delete(request,pk):
    teacher = Teacher.objects.get(pk=pk)
    student_delete_form = Teacher.objects.get(pk=pk)
    if request.method == 'POST':
        student_delete_form.delete()
        return redirect('parachapp:teacher_home')
    context = {
        'student_delete_form':student_delete_form,
        'teacher':teacher
    }

    return render(request, 'staff_template/teacher_delete.html',context)