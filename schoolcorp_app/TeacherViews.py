from django.shortcuts import render,redirect,get_object_or_404
from schoolcorp_app.models import Teacher, Post, Comment, Notification
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CommentForm

def calculate_profile_completeness(teacher):
    required_fields = [
        'admin__username', 'admin__email', 'mobile_no', 'date_of_birth', 'gender',
        'designation', 'father_name', 'mother_name', 'qualification', 'maritalStatus',
        'permanent_address', 'workExperience', 'Current_Address', 'profile_pic', 'banner',
        'institution_type', 'resume', 'join_date', 'city', 'state', 'pin', 'fb', 'insta',
        'linkdin'
    ]
    # We will assume equal weight for simplicity
    field_weight = 1 / len(required_fields)

    completeness = 0
    for field in required_fields:
        value = getattr(teacher, field.replace('admin__', 'admin.'), None)
        if value:
            completeness += field_weight

    completeness_percentage = int(completeness * 100)
    return completeness_percentage

# def get_nearby_teachers(admin_user):
#     try:
#         teacher = Teacher.objects.get(admin=admin_user)
#         nearby_teachers = Teacher.objects.filter(state=teacher.state).exclude(admin=admin_user)
#         return nearby_teachers
#     except Teacher.DoesNotExist:
#         return None


def teacher_home(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)
    
    completeness_percentage = calculate_profile_completeness(teacher)
    posts = Post.objects.all().select_related('user__teacher', 'user__employee', 'user__school').order_by('-created_at')
    
    
    context = {
        "teacher": teacher, 
        'completeness_percentage': completeness_percentage, 
        'posts': posts, 
        'comment_form': CommentForm(),
        
    }
    
    return render(request, "teacher_template/home.html", context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            # Create notification
            if post.user != request.user:
                # Notification model and creation code here
                pass
            # Return JSON response
            return JsonResponse({
                'user_profile_pic': request.user.teacher.profile_pic.url if request.user.teacher.profile_pic else '',
                'user_first_name': request.user.first_name,
                'user_last_name': request.user.last_name,
                'date_added': comment.date_added,
                'comment_body': comment.body
            })
    return HttpResponseBadRequest()

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:  # Ensure the user is the owner of the post
        post.delete()
    return redirect('teacher_home')

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:  # Ensure the user is the owner of the comment
        comment.delete()
    return redirect('teacher_home') 

    

def teacher_profile_pic_update(request):
    if request.method == "POST":
        user_profile = Teacher.objects.get(admin_id=request.user)
        profile_pic = request.FILES.get("profile_pic")

        if profile_pic:
            user_profile.profile_pic.save(profile_pic.name, profile_pic)
            user_profile.save()
            return redirect('teacher_home')  # Render the template on successful upload
        else:
            return HttpResponse("No profile picture provided.")

    return HttpResponse("Method Not allowed")

def banner_update_teacher(request):
    if request.method == "POST":
        try:
            user_profile = Teacher.objects.get(admin=request.user)
        except ObjectDoesNotExist:
            return HttpResponse("User profile not found.")

        banner = request.FILES.get("banner")

        if banner:
            user_profile.banner = banner
            user_profile.save()
            return redirect('teacher_home')  
        else:
            return HttpResponse("No banner provided.")
    else:
        return HttpResponse("Method Not Allowed")
    

def doPostt(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        post_text = request.POST.get('postText')
        post_img = request.FILES.get('postImg')
        user_id = request.POST.get('userID')

        try:
            post = Post(user_id=user_id, text_post=post_text, post_img=post_img)
            post.save()
            return redirect('teacher_home')
        except Exception as e:
            return HttpResponse(f"Error saving post: {e}")
        


def complete_profile(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)

    completeness_percentage = calculate_profile_completeness(teacher)

    context = {"teacher": teacher, 'completeness_percentage': completeness_percentage}
    return render(request, "teacher_template/profile.html",context)

   


def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
            # Create notification
            if post.user != user:
                Notification.objects.create(
                    user=post.user,
                    post=post,
                    text=f'{user.first_name} {user.last_name} liked your post.'
                )
        
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
    return HttpResponse("Invalid request method", status=400)


def update_teacher(request):
    if request.method == "POST":
        try:
            user_profile = Teacher.objects.get(admin=request.user)
        except ObjectDoesNotExist:
            return HttpResponse("User profile not found.")
        
        # Update user_profile with the form data
        date_of_birth = request.POST.get("date_of_birth")
        join_date = request.POST.get("join_date")
        if date_of_birth:
            user_profile.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            user_profile.join_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        user_profile.mobile_no = request.POST.get("mobile_no")
        user_profile.linkdin = request.POST.get("linkdin")
        user_profile.insta = request.POST.get("insta")
        user_profile.fb = request.POST.get("fb")
        user_profile.gender = request.POST.get("gender")
        user_profile.designation = request.POST.get("designation")
        user_profile.institution_type = request.POST.get("institution_type")
        user_profile.resume = request.FILES.get("resume")
        user_profile.city = request.POST.get("city")
        user_profile.state = request.POST.get("state")
        user_profile.pin = request.POST.get("pin")
        user_profile.father_name = request.POST.get("father_name")
        user_profile.mother_name = request.POST.get("mother_name")
        user_profile.qualification = request.POST.get("qualification")
        user_profile.maritalStatus = request.POST.get("maritalStatus")
        user_profile.permanent_address = request.POST.get("permanent_address")
        user_profile.workExperience = request.POST.get("workExperience")
        user_profile.Current_Address = request.POST.get("current_Address")
        # Save the updated profile
        user_profile.save()
        
        return redirect('profile')


        
        
def update_teacher_profile(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)

    completeness_percentage = calculate_profile_completeness(teacher)

    context = {"teacher": teacher, 'completeness_percentage': completeness_percentage}
    return render(request, "teacher_template/update_profile.html",context)
        

def timeline_photo(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)
    teacher = Teacher.objects.get(admin_id=teacher.admin_id)
    
    # Retrieve posts where the user_id matches the admin_id of the teacher
    post_img = Post.objects.filter(user_id=teacher.admin_id).values_list('post_img', flat=True)
    completeness_percentage = calculate_profile_completeness(teacher)
    
    context = {"teacher": teacher, 'completeness_percentage': completeness_percentage, 'post_img': post_img}
    return render(request, "teacher_template/timeline_photo.html",context)        



def about(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)

    completeness_percentage = calculate_profile_completeness(teacher)

    context = {"teacher": teacher, 'completeness_percentage': completeness_percentage}
    return render(request, "teacher_template/about.html",context)




def resume(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)
    teacher = Teacher.objects.get(admin_id=teacher.admin_id)
    completeness_percentage = calculate_profile_completeness(teacher)
    
  
    
    context = {
        "teacher": teacher,
        'completeness_percentage': completeness_percentage,
        
    }
    
    return render(request, "teacher_template/resume.html", context)


def change_password(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)

    completeness_percentage = calculate_profile_completeness(teacher)

    context = {"teacher": teacher, 'completeness_percentage': completeness_percentage}
    return render(request, "teacher_template/change_password.html",context)

def notification(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)

    completeness_percentage = calculate_profile_completeness(teacher)
    context = {"teacher": teacher,'completeness_percentage': completeness_percentage}
    return render(request, "teacher_template/notification.html",context)


@login_required
def password_change(request):
    admin_user = request.user
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if the new passwords match
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return render(request, "teacher_template/change_password.html")
        
        # Check if the current password is correct
        if not check_password(current_password, admin_user.password):
            messages.error(request, "Current password is incorrect.")
            return render(request, "teacher_template/change_password.html")
        
        # Set the new password and save the user
        admin_user.set_password(new_password)
        admin_user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, admin_user)
        
        messages.success(request, "Password updated successfully.")
        return redirect('change_password')  # Redirect to a suitable page
    
    # Ensure the teacher profile exists
    try:
        teacher = Teacher.objects.get(admin=admin_user)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher profile not found.")
        return redirect('change_password')
    
    return render(request, "teacher_template/change_password.html")


def people_nearby(request):
    admin_user = request.user
    teacher = Teacher.objects.get(admin=admin_user)

    completeness_percentage = calculate_profile_completeness(teacher)

    context = {"teacher": teacher, 'completeness_percentage': completeness_percentage}
    return render(request, "teacher_template/people_nearby.html",context)
# def recent_activity(request):
#     admin_user = request.user
#     teacher = Teacher.objects.get(admin=admin_user)

#     completeness_percentage = calculate_profile_completeness(teacher)
#     activities = Activity.objects.filter(user=request.user).order_by('-created_at')

#     context = {"teacher": teacher, 'completeness_percentage': completeness_percentage, "activities": activities}
#     return render(request, "teacher_template/recent_activity.html",context)

