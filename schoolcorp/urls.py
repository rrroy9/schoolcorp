"""
URL configuration for schoolcorp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from schoolcorp import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include



from schoolcorp_app import views, AdminViews, SchoolViews, TeacherViews

urlpatterns = [
                  path('', views.index, name='index'),
                  path('accounts/',include('django.contrib.auth.urls')),
                  path('login/', views.ShowLogin, name='login'),
                  path('admin/', admin.site.urls),
                  path('doLogin', views.doLogin, name='doLogin'),
                  path('GetUserDetails', views.GetUserDetails, name='GetUserDetails'),
                  path('logout_user', views.logout_user, name='logout_user'),
                  path('school_home', SchoolViews.school_home, name='school_home'),
                  path('teacher_home', TeacherViews.teacher_home, name='teacher_home'),
                  path('job_post', SchoolViews.post_job, name='post_job'),
                  # path('school_dashboard_home', SchoolViews.school_dashboard_home, name='school_dashboard_home'),
                  path('update_school_profile_pic/', SchoolViews.school_profile_pic_update, name='update_school_profile_pic'),
                  path('banner_update', SchoolViews.UpdateBanner, name='banner_update'),
                  path('doPost', SchoolViews.doPost, name='doPost'),
                  path('add_employee', AdminViews.add_employee, name='add_employee'),
                  path('admin_home', AdminViews.admin_home, name='admin_home'),
                  path('employee_register', AdminViews.employee_register, name='employee_register'),
                  path('contact_us', views.contact_us, name='contact_us'),
                  path('about_us_page', views.about_us_page, name='about_us_page'),
                  path('contact_us_page', views.contact_us_page, name='contact_us_page'),
                  path('banner_update_teacher', TeacherViews.banner_update_teacher, name='banner_update_t'),
                  path('teacher_profile_pic_update', TeacherViews.teacher_profile_pic_update, name='teacher_profile_pic'),
                  path('doPostt', TeacherViews.doPostt, name='doPostt'),
                  path('checkemail/', views.check_email_existence, name='check_email_existence'),
                  path('send_otp', views.send_otp, name='send_otp'),
                  path('checkusername', views.checkusername, name='checkusername'),
                  path('verify_otp', views.verify_otp, name='verify_otp'),
                  path('create_user', views.create_user, name='create_user'),  
                  path('add_schools', AdminViews.add_schools, name='add_schools'),
                  path('complete_profile', TeacherViews.complete_profile, name='profile'),  
                  path('post_like/<int:pk>/', TeacherViews.post_like, name='post_like'),
                  path('add_school', AdminViews.add_school, name='add_school'), 
                  path('update_teacher',TeacherViews.update_teacher,name='update_teacher'),
                  path('message',AdminViews.message,name='message'),
                  path('update_teacher_profile',TeacherViews.update_teacher_profile,name='update_teacher_profile'),
                  path('timeline_photo',TeacherViews.timeline_photo,name='timeline_photo'),
                #   path('chart_data/', AdminViews.chart_data, name='chart_data'),
                  path('request-otp/', views.request_otp, name='request_otp'),
                  path('verify_otp_two/', views.verify_otp_two, name='verify_otp_two'),
                  path('update-password/', views.update_password, name='update_password'),
                  path('about', TeacherViews.about, name='about'),
                  path('resume', TeacherViews.resume, name='resume'),
                  path('change_password', TeacherViews.change_password, name='change_password'),
                  path('password_change', TeacherViews.password_change, name='password_change'),
                #   path('recent_activity', TeacherViews.recent_activity, name='recent_activity')
                  path('post/<int:post_id>/comment/', TeacherViews.add_comment, name='add_comment'),
                  path('delete-post/<int:post_id>/', TeacherViews.delete_post, name='delete_post'),
                  path('delete-comment/<int:comment_id>/', TeacherViews.delete_comment, name='delete_comment'),
                  path('notification', TeacherViews.notification, name='notification'),
                  path('people_nearby', TeacherViews.people_nearby, name='people_nearby'),
                  

              ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)