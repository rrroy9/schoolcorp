from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Employee"), (3, "School"), (4, "Teacher"),
                      )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    otp = models.CharField(max_length=6, blank=True, null=True)


@property
def profile(self):
    if hasattr(self, 'adminhod'):
        return self.adminhod
    elif hasattr(self, 'employee'):
        return self.staff
    elif hasattr(self, 'school'):
        return self.school
    elif hasattr(self, 'teacher'):
        return self.teacher
    else:
        return None
    
@property
def profile_pic_url(self):
    try:
        if hasattr(self, 'teacher'):
            return self.teacher.profile_pic.url
        elif hasattr(self, 'employee'):
            return self.employee.profile_pic.url
        elif hasattr(self, 'school'):
            return self.school.profile_pic.url
    except ValueError:
        return None
    return None    


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()





class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='employee')
    profile_pic = models.ImageField(upload_to='images/')
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_no = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    designation = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    maritalStatus = models.CharField(max_length=10)
    permanent_address = models.CharField(max_length=255)
    workExperience = models.CharField(max_length=255)
    Current_Address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    



class School(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='school')
    school_name = models.CharField(max_length=45)
    mobile_no = models.CharField(max_length=45)
    profile_pic = models.ImageField(null=True, upload_to='profile_pics/')
    banner = models.ImageField(null=True,upload_to='banners/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    

class TeacherManager(models.Manager):
    def nearby_teachers(self, state):
        return self.filter(state=state)

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='teacher')
    profile_pic = models.ImageField(upload_to='profile_pics/')
    banner = models.ImageField(upload_to='banners/')
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_no = models.CharField(max_length=45)
    gender = models.CharField(max_length=10)
    designation = models.CharField(max_length=45)
    institution_type = models.CharField(max_length=45,null=True)
    resume = models.FileField(upload_to='banners/', blank=True, null=True)
    join_date = models.CharField(max_length=45, null=True)
    city = models.CharField(max_length=45, null=True)
    state = models.CharField(max_length=45, null=True)
    pin = models.CharField(max_length=45, null=True)
    fb = models.CharField(max_length=45,null=True)
    insta = models.CharField(max_length=45,null=True)
    linkdin = models.CharField(max_length=45,null=True)
    father_name = models.CharField(max_length=45)
    mother_name = models.CharField(max_length=45)
    qualification = models.CharField(max_length=45)
    maritalStatus = models.CharField(max_length=10)
    permanent_address = models.CharField(max_length=225)
    workExperience = models.CharField(max_length=45)
    Current_Address = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    objects = TeacherManager()


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,related_name="posts",on_delete=models.DO_NOTHING)
    text_post = models.TextField(null=True)
    post_img = models.ImageField(null=True, upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)
    objects = models.Manager()

    def number_of_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)   
    
  

class Contactus(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name="notifications", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="notifications", on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, related_name="notifications", on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text    



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type == 2:
            Employee.objects.create(admin=instance)
        elif instance.user_type == 3:
            School.objects.create(admin=instance)
        elif instance.user_type == 4:
            Teacher.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.employee.save()
    if instance.user_type == 3:
        instance.school.save()
    if instance.user_type == 4:
        instance.teacher.save()
