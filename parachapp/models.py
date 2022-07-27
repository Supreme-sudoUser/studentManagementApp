from django.contrib.auth.models import AbstractUser
from django.core.checks import messages
from django.db import models
from django.db.models.base import Model
from django.db.models.expressions import OrderBy

#from django.core.validators import RegexValidator
#from django.core.validators import MinValueValidator, MaxValueValidator

from twilio.rest import Client
from decimal import Decimal
import re
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class StudySession(models.Model):
    session_start = models.DateField(null=True, blank=True)
    session_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.session_start} = to = {self.session_end}'

class Course(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default='0000000.00', null=True, blank=True)
    
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    mobile_phone = models.BigIntegerField(blank=True, null=True, default='070')
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    bio = models.TextField(null = True, blank=True, default='write about yourself here (optional)')
    
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender = models.CharField(max_length=7, choices=GENDER, default='Male')
    profile_pic = models.ImageField( upload_to = 'Profile_pics', null = True, blank = True)
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    #amountpaid = models.DecimalField(max_digits=9, decimal_places=2, default='000000.00',null=True, blank=True)
    
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)

    
    
    '''
    validate = r"^[189][0-9]{7}$"
    phone_number = input()
    valid = re.search(validate, phone_number)
    if valid:
        print("Valid")
    else:
        print("Invalid")
    
    
    '''
class StudentAdvancedProfile(models.Model):
    studentinstance = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    amountpaid = models.DecimalField(max_digits=8, decimal_places=2, default='0000000.00',null=True, blank=True)
    
    STATUS = (
        ('Fully Paid', 'Fully Paid'),
        ('Not Fully Paid', 'Not Fully Paid'),
        ('Not Paid','Not Paid'),
    )
    payment_status = models.CharField(max_length=16, choices=STATUS, default="Not Paid")
    completed_course = models.BooleanField(default=False, null=True, blank=True)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.studentinstance.firstname

  

    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    mobile_phone = models.BigIntegerField(blank=True, null=True, default='070')
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    profile_pic = models.FileField( upload_to = 'Profile_pics', null = True, blank = True)
    GENDER = (
        ('m', 'male'),
        ('f', 'female')
    )
    gender = models.CharField(max_length=5, choices=GENDER, default='male')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
   
    added_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class Salary(models.Model):
    teacherinstance = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default='0000000.00', null=True, blank=True)
    date_paid = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.teacherinstance.firstname}, {self.amount}' 

class UploadFile(models.Model):
    teacherinstance = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file_title = models.CharField(max_length=120)
    files = models.FileField(upload_to='media', null=True)
    uploaded_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.teacherinstance.firstname} - {self.course.name}'

    @property
    def filesURL(self):
        try:
            url = self.files.url
        except:
            url = ''
        return url



class Message(models.Model):
     sender = models.ForeignKey(Teacher, on_delete=models.CASCADE)
     reciever = models.ForeignKey(Student, on_delete=models.CASCADE)
     msg_content = models.TextField() 
     created_at = models.DateField(auto_now_add=True)



class Attend(models.Model):
    attender = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_present = models.DateField(null=True, blank=True)

    def __str__(self):

        return str(f'{self.date_present} - {self.attender.firstname}')

class Notification(models.Model):
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    is_true = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return str(self.date_sent)
    
    def save(self, *args, **kwargs):
        if self.is_true == True:
            account_sid = 'AC44247dd330ca46ad388ca9b6041c2f1d'
            auth_token = 'b708564915f0068c13ac3d9b0877d139'
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                body=f"(From parach computers) Hello {self.student_name.firstname}, {self.message}",
                                from_='+12103618147',
                                to=f'+234{self.student_name.mobile_phone}'
                            )

            print(message.sid)

        return super().save(*args, **kwargs)

#Creating Django Signals where the Student is the sender and StudentAdvancedProfile is the receiver
@receiver(post_save, sender=Student)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.studentadvancedprofile_set.create(studentinstance=instance.firstname, course=Course.objects.get(id=1),session=StudySession.objects.get(id=1))
        print('=================instance created')


    