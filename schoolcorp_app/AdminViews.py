from datetime import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from schoolcorp_app.models import Teacher, Employee,School,Contactus
from django.db.models import Count
from .models import CustomUser
from django.db.models.functions import ExtractMonth




def add_employee(request):
    return render(request, "Admin_template/add_employe.html")


def admin_home(request):
    # Count the total number of instances for each model
    employee_count = Employee.objects.count()
    school_count = School.objects.count()
    teacher_count = Teacher.objects.count()

    today = datetime.now().date()
    new_teachers_today = Teacher.objects.filter(created_at__date=today).count()
    new_schools_today = School.objects.filter(created_at__date=today).count()
    

    context = {
        'employee_count': employee_count,
        'school_count': school_count,
        'teacher_count': teacher_count,
        'new_teachers_today': new_teachers_today,
        'new_schools_today': new_schools_today,
        
        
    }
    
    return render(request, "Admin_template/admin_home.html", context)


def employee_register(request):
    if request.method != "POST":
        return HttpResponse("Method Not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        profile_pic = request.FILES["profile_pic"]
        date_of_birth = request.POST.get("date_of_birth")
        mobile_no = request.POST.get("mobile_no")
        designation = request.POST.get("designation")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        qualification = request.POST.get("qualification")
        maritalStatus = request.POST.get("maritalStatus")
        permanent_address = request.POST.get("permanent_address")
        workExperience = request.POST.get("work_experience")
        Current_Address = request.POST.get("Current_Address")
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            error_message = "Username or email already exists."
            messages.error(request, f"Error: {error_message}")
            return JsonResponse({"success": False, "error_message": error_message})

        try:
            # Create the CustomUser instance
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2  # Assuming 2 is for Staff according to the previous model
            )

            # Create and associate the Staff instance
            user.employee.profile_pic = profile_pic
            user.employee.date_of_birth = date_of_birth
            user.employee.mobile_no = mobile_no
            user.employee.gender = gender
            user.employee.designation = designation
            user.employee.father_name = father_name
            user.employee.mother_name = mother_name
            user.employee.qualification = qualification
            user.employee.maritalStatus = maritalStatus
            user.employee.permanent_address = permanent_address
            user.employee.workExperience = workExperience
            user.employee.Current_Address = Current_Address
            user.employee.save()

            messages.success(request, "Successfully Added")
            return HttpResponseRedirect('/add_employe')
        except ValidationError as e:
            messages.error(request, str(e))
            return HttpResponseRedirect('/add_employe')
        except:
            messages.error(request, "Invalid error")
            return HttpResponseRedirect('/add_employe')


def add_schools(request):
    return render(request, "Admin_template/add_school.html")


def add_school(request):
    if request.method != "POST":
        return HttpResponse("Method Not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            error_message = "Username or email already exists."
            messages.error(request, f"Error: {error_message}")
            return JsonResponse({"success": False, "error_message": error_message})

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=3)
            user.save()
            messages.success(request, "Successfully Added")
            return JsonResponse({"success": True})

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return JsonResponse({"success": False, "error_message": str(e)})
        
def add_school(request):
    if request.method == "POST":
        # Extract data from the form
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
       
        # Check if the username or email already exists
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            error_message = "Username or email already exists."
            messages.error(request, error_message)
            return redirect('add_school')  # Redirect to the same page or to a different page

        try:
            # Create the CustomUser instance
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=3  # Assuming 3 is for School according to your model
            )
            

            user.save()

            messages.success(request, "School added successfully")
            return redirect('add_schools')  # Redirect to the same page or to a different page

        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('add_schools')  # Redirect to the same page or to a different page

    else:
        return render(request, "Admin_template/add_school.html")        
    

def message(request):
    # Retrieve all Contactus objects ordered by created_at in descending order
    contacts = Contactus.objects.order_by('-created_at')
    # Pass the retrieved data to the template context
    return render(request, "Admin_template/message.html", {"contacts": contacts})


# def chart_data(request):
#     # Query the database to count the number of schools created in each month
#     school_data = (
#         School.objects
#         .annotate(month=ExtractMonth('created_at'))
#         .values('month')
#         .annotate(count=Count('id'))
#         .order_by('month')
#         .values_list('count', flat=True)
#     )

#     # Query the database to count the number of teachers registered in each month
#     teacher_data = (
#         Teacher.objects
#         .annotate(month=ExtractMonth('created_at'))
#         .values('month')
#         .annotate(count=Count('id'))
#         .order_by('month')
#         .values_list('count', flat=True)
#     )

    

#     data = {
#         'school_data': list(school_data),
#         'teacher_data': list(teacher_data),
        
#     }

#     return JsonResponse(data)
