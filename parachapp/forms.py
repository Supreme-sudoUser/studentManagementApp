from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.db import transaction
from django.db.models import fields
from parachapp import models

from parachapp.models import (Salary, Student, Teacher, User, 
                                Attend,Course, 
                                StudySession,Notification,
                                StudentAdvancedProfile,
                                UploadFile
                                )
from django.core.exceptions import ValidationError
import datetime
from datetime import date



class StudentSignUpForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'create a username'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))
    
    class Meta(UserCreationForm.Meta):
        model = User

    #@transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user, profile_pic='Profile_pics/2.jpg')
        
        #student.interests.add(*self.cleaned_data.get('interests'))
        return user


#student account update
class StudentAccountChangeUpdate(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'create a username'}))
    
    class Meta:
        model = User
        fields = [
            'username',
        ]

class StudentUpdateForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'firstname',
            'lastname',
            'email',
            'address',
            'gender',
            'bio',
            'profile_pic',
            'mobile_phone',
            
            ]



class StudentAdvancedProfileForm(forms.ModelForm):
    class Meta:
        model = StudentAdvancedProfile
        fields = [
            'session',
            'course',
            'amountpaid',
            'payment_status',
            'completed_course'
        ]  

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attend
        exclude = ['attender']



class TeacherSignUpForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'create a username'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))
    
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        #if commit:
          #  user.save()
        teacher = Teacher.objects.create(user=user,course=Course.objects.get(id=1), profile_pic='Profile_pics/3.jpg')
        return user

#teacher account update
class TeacherAccountChangeUpdate(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'create a username'}))
    
    class Meta:
        model = User
        fields = [
            'username',
        ]

class TeacherUpdateForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [
            'firstname',
            'lastname',
            'mobile_phone',
            'email',
            'address',
            'gender',
            'course',
            'profile_pic',
            
            ]

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = [
            'teacherinstance',
            'course',
            'file_title',
            'files',
            ]

class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = '__all__'

    def clean_is_true(self):
        messages_check = self.cleaned_data['is_true']
        if messages_check == False:
             raise ValidationError(f'The box must be checked to proceed to send your message, thank you!')
        return messages_check

#course creation form
class CreateStudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = [
            'session_start',
            'session_end'
        ]

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name',
            'price',
        ]
        
class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name',
            'price',
            
        ]


class PaySalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'amount',
        ]

class UpdateSalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'amount',
        ]