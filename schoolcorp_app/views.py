import json
from django.contrib.auth import logout, login
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import JsonResponse
from schoolcorp_app.EmailBackEnd import EmailBackEnd  # Replace with your actual EmailBackEnd import
from django.contrib import messages
from schoolcorp_app.models import CustomUser, Contactus
from django.urls import reverse
import pyotp
import logging
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.contrib.staticfiles import finders
from .forms import OTPRequestForm, OTPVerificationForm, PasswordResetForm
from django.core.mail import send_mail
import random



logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'home_content/index.html')


def ShowLogin(request):
    return render(request, 'home_content/login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse('admin_home'))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("employee_home"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("school_home"))
            elif user.user_type == "4":
                return HttpResponseRedirect(reverse("teacher_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect(reverse("login"))


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User :" + request.user.email + "Usertype: " + request.user.user_type)
    else:
        return HttpResponse('Login First')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")





def contact_us(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        try:
            user = Contactus(full_name=full_name, email=email, message=message)
            user.save()
            messages.success(request, "Successfully Added")
            return HttpResponseRedirect('/')  # Redirect to the home page
        except ValidationError as e:
            messages.error(request, str(e))
            return HttpResponseRedirect('/')  # Redirect to the home page
        except:
            messages.error(request, "An error occurred")
            return HttpResponseRedirect('/')  # Redirect to the home page

def about_us_page(request):
    return render(request, 'home_content/about_us_page.html')        

def contact_us_page(request):
    return render(request, 'home_content/contact_us_page.html')

def check_email_existence(request):
     if request.method == 'GET':
        email = request.GET.get('email')
        if email:
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'exists': True})
            else:
                return JsonResponse({'exists': False})
        else:
            return JsonResponse({'error': 'Email parameter missing'}, status=400)
     else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def checkusername(request):
    username = request.GET['username']
    try:
        CustomUser.objects.get(username=username)
        return HttpResponse('true')
    except:
        return HttpResponse('false')
    

def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        logo_path = finders.find('media/logo2.png')
        
        # Generate OTP
        totp = pyotp.TOTP(pyotp.random_base32())
        otp = totp.now()
        
        # Save OTP in session
        request.session['otp'] = otp
        
        # Render HTML content from template
        html_content = render_to_string('otp_template/otp.html', {'otp': otp, 'logo': logo_path})
        
        # Send email
        subject = 'Your OTP'
        sender_email = 'support@schoolcorp.in'  # Replace with your sender email
        
        # Strip the HTML tags for plain text email
        plain_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(subject, plain_content, sender_email, [email])
        email.attach_alternative(html_content, "text/html")  # Attach HTML content
        
        try:
            email.send()
            return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})
        except Exception as e:
            logger.error(f"Failed to send OTP to {email}: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            otp = data.get('otp')

            # Retrieve the OTP sent to the user from the session
            sent_otp = request.session.get('otp')

            if sent_otp and otp == sent_otp:  # Compare the OTPs
                # Clear OTP from session after successful verification
                del request.session['otp']
                return JsonResponse({'status': 'success', 'message': 'OTP verified successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data in request.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
    

def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        
        try:
            # Create the user without hashing the password
            user = CustomUser.objects.create_user(email=email, password=password, 
                                                   first_name=first_name, last_name=last_name,
                                                   username=username, user_type=4)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'User created successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)




def request_otp(request):
    if request.method == 'POST':
        form = OTPRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = random.randint(100000, 999999)
                user.otp = str(otp)
                user.save()
                send_mail(
                    'Your OTP',
                    f'Your OTP is {otp}',
                    'support@schoolcorp.in',  # Sender email address
                    [email],
                    fail_silently=False,
                )
                request.session['email'] = email
                return redirect('verify_otp_two')
            except CustomUser.DoesNotExist:
                return render(request, 'request_otp.html', {'form': form, 'error': 'User with this email does not exist.'})
        else:
            return render(request, 'request_otp.html', {'form': form, 'error': 'Invalid form data.'})
    else:
        form = OTPRequestForm()
        return render(request, 'request_otp.html', {'form': form})




def verify_otp_two(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            email = request.session.get('email')
            otp = form.cleaned_data['otp']
            try:
                user = CustomUser.objects.get(email=email)
                if user.otp == otp:
                    request.session['verified'] = True
                    return redirect('update_password')
                else:
                    messages.error(request, 'Invalid OTP.')
                    return render(request, 'verify_otp.html', {'form': form})
            except CustomUser.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
                return render(request, 'verify_otp.html', {'form': form})
        else:
            messages.error(request, 'Invalid form data.')
            return render(request, 'verify_otp.html', {'form': form})
    else:
        form = OTPVerificationForm()
        return render(request, 'verify_otp.html', {'form': form})


    

def update_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            if request.session.get('verified'):
                email = request.session.get('email')
                new_password = form.cleaned_data['new_password']
                try:
                    user = CustomUser.objects.get(email=email)
                    user.set_password(new_password)
                    user.otp = ''  # Clear OTP after successful password reset
                    user.save()
                    messages.success(request, 'Password updated successfully.')
                    return redirect('login')
                except CustomUser.DoesNotExist:
                    messages.error(request, 'User with this email does not exist.')
                    return render(request, 'update_password.html', {'form': form})
            else:
                messages.error(request, 'OTP verification required.')
                return redirect('request_otp')
        else:
            messages.error(request, 'Invalid form data.')
            return render(request, 'update_password.html', {'form': form})
    else:
        form = PasswordResetForm()
        return render(request, 'update_password.html', {'form': form})