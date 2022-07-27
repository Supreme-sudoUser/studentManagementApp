from django.urls import path
from . import views
from parachapp import admin_views
from parachapp import staff_views
from parachapp import student_views

app_name = 'parachapp'
urlpatterns = [
    path('index/', views.index, name='index'),
    
    path('register_student/', views.student_sign_up, name='reg_student'),
    path('account-successful/', views.success_account, name='success'),
    path('register_teacher/', views.teacher_sign_up, name='reg_teacher'),
    path('', views.login_request, name='login'),
    path('logout/', views.logout_request, name= 'logout'),
    
    path('student-home/', views.student_home, name='student_home'),
    path('teacher-home/', views.teacher_home, name='teacher_home'),
    

    #admin views
    path('home/', admin_views.adminhome, name='dashboard' ),

    #file download
    path('download/', admin_views.fileupload, name='fileupload' ),
    

    #teachers salary
    path('salaryhome/', admin_views.salaryhome, name='salaryhome'),
    path('update_salary/<str:pk>/', admin_views.update_salary, name='update_salary' ),
    path('delete_salary/<str:pk>/', admin_views.delete_salary, name='delete_salary' ),

    path('liveclass/', admin_views.liveclass, name='liveclass' ),
    path('notify/', admin_views.notifications, name='notify'),
    path('create_teacher/', admin_views.create_teacher, name='create_teacher'),
    path('create_student/', admin_views.create_student, name='create_student'),
    path('create_course/', admin_views.create_course, name='create_course'),

    path('payment_stat/', admin_views.payment_stat, name='payment_stat'),

    path('update_course/<str:pk>/', admin_views.update_course, name='update_course'),
    path('delete_course/<str:pk>/', admin_views.delete_course, name='delete_course'),
    

    #teachers views
    path('teacher/<str:pk>/', staff_views.teacher_detail, name='teacher_details'),
    path('update-teacher/<str:pk>/', staff_views.teacher_update, name='teacher_updates'),
    path('teacher_delete/<str:pk>/', staff_views.teacher_delete, name='teacher_delete'),
   

    #student views
    path('student_detail/<str:pk>/', student_views.student_detail, name='student_details'),
    path('update-student/<str:pk>/', student_views.student_update, name='student_updates'),
    path('advanced/<str:pk>/', student_views.student_advanced_update, name='advanced_updates'),
    path('student_delete/<str:pk>/', student_views.student_delete, name='student_delete'),
]