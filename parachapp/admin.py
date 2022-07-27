from django.contrib import admin
from parachapp.models import (Attend, Salary,
                    User,Student,
                    Teacher,StudySession,
                    Course,Notification,
                    StudentAdvancedProfile,
                    Salary,UploadFile

                    )
# Register your models here.


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Attend)
admin.site.register(StudySession)
admin.site.register(Course)
admin.site.register(Notification)
admin.site.register(StudentAdvancedProfile)
admin.site.register(Salary)
admin.site.register(UploadFile)

