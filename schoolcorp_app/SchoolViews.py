from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from schoolcorp_app.models import School, Post


def school_home(request):
    admin_user = request.user
    school = School.objects.get(admin=admin_user)
    
    
    posts = Post.objects.all().select_related('user__teacher', 'user__employee', 'user__school').order_by('-created_at')
    
    context = { "school": school,  'posts': posts }
    
    return render(request, "school_template/home.html", context)


def post_job(request):
    return render(request, "school_template/post_job.html")


def school_profile_pic_update(request):
    if request.method == "POST":
        try:
            user_profile = School.objects.get(admin=request.user)
        except ObjectDoesNotExist:
            return HttpResponse("User profile not found.")
        
        profile_pic = request.FILES.get("profile_pic")

        if profile_pic:
            user_profile.profile_pic.save(profile_pic.name, profile_pic)
            user_profile.save()
            return redirect('school_home')  # Adjust this to your desired redirect URL
        else:
            return HttpResponse("No profile picture provided.")
    return HttpResponse("Method Not Allowed")


def UpdateBanner(request):
    if request.method == "POST":
        try:
            user_profile = School.objects.get(admin=request.user)
        except ObjectDoesNotExist:
            return HttpResponse("User profile not found.")

        banner = request.FILES.get("banner")

        if banner:
            user_profile.banner = banner
            user_profile.save()
            return redirect('school_home')  # Redirect to the 'school_home' page
        else:
            return HttpResponse("No banner provided.")
    else:
        return HttpResponse("Method Not Allowed")


def doPost(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        post_text = request.POST.get('postText')
        post_img = request.FILES.get('postImg')
        user_id = request.POST.get('userID')

        try:
            post = Post(user_id=user_id, text_post=post_text, post_img=post_img)
            post.save()
            return redirect('school_home')
        except Exception as e:
            return HttpResponse(f"Error saving post: {e}")