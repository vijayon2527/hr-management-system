import hashlib
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import authenticate, login
from .models import User
from .forms import UserRegistrationForm, OTPVerificationForm, LoginForm
from .functions.otp_utils import (
    generate_otp, 
    send_otp_to_mobile, 
    send_otp_to_email, 
    set_registration_session, 
    SESSION_REGISTRATION_KEY
)

from applicant.models import Applicant

class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            raise Http404('you are already logged in !!!')
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            mobile_number = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')
           
            # TODO otp verification============================================================
            # otp = generate_otp()
            # if mobile_number:
            #     send_otp_to_mobile(mobile_number, otp)
            # elif email:
            #     send_otp_to_email(email, otp)
            
            # set_registration_session(request, otp, mobile_number or email, user_type, password)
            # return redirect('users:otp_verification')
            # TODO remove this code 
            user = User.objects.create_user(
                    mobile=mobile_number,
                    user_type=user_type
                )
            user.set_password(password)
            user.save()
            login(request, user, backend='users.backend.EmailOrMobileBackend')
            messages.success(request, "Your account is created and logged in successfully.")
            return redirect('redirect_url')
            # ==================================================================================
        else:
            return render(request, self.template_name, {'form': form})
# This is currently not using
def register_view(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST, request.FILES) 
        if form.is_valid():
            # Extract data from the form

            user_data = {
                'mobile_number': form.cleaned_data.get('mobile'),
                'password': form.cleaned_data.get('password1'),
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'date_of_birth': form.cleaned_data.get('date_of_birth'),
                'address_line_1': form.cleaned_data.get('address_line_1'),
                'city': form.cleaned_data.get('city'),
                'state': form.cleaned_data.get('state'),
                'postal_code': form.cleaned_data.get('postal_code'),
                'resume': form.cleaned_data.get('resume'),
            }
            # Create the user
            user = User.objects.create_user(
                mobile=user_data['mobile_number'],
            )
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.date_of_birth = user_data['date_of_birth']
            user.address_line_1 = user_data['address_line_1']
            user.city = user_data['city']
            user.state = user_data['state']
            user.postal_code = user_data['postal_code']  
            user.set_password(user_data['password'])
            user.save()
            resume = user_data['resume']
            Applicant.objects.create(user=user, resume=resume)
            messages.success(request, "Your account has been created successfully.")
            return redirect('redirect_url')
        else:
            messages.error(request, "invalid form")
            return render(request, 'users/register.html', {'form': form})
    else:
        if request.user.is_authenticated:
            raise Http404('You are already logged in!')
        
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

class OTPVerificationView(View):
    template_name = 'users/verify_otp.html'

    def get(self, request):
        if not request.session.get(SESSION_REGISTRATION_KEY):
            raise Http404
        form = OTPVerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        
        if not form.is_valid():
            messages.error(request, "Invalid form data")
            return render(request, self.template_name, {'form': form})
        
        entered_otp = form.cleaned_data.get('otp_code')
        session_data = request.session.get(SESSION_REGISTRATION_KEY)
        
        if not session_data:
            messages.error(request, "OTP is expired or invalid.")
            return redirect('users:register')
        
        stored_otp = session_data.get('otp')
        identifier = session_data.get('identifier')
        user_type = session_data.get('user_type')
        password = session_data.get('password')
        entered_otp_hashed = hashlib.sha256(entered_otp.encode()).hexdigest()
        
        if stored_otp and identifier and entered_otp_hashed == stored_otp:
            try:
                user = User.objects.create_user(
                    email=identifier if '@' in identifier else None,
                    mobile=identifier if not '@' in identifier else None,
                    user_type=user_type
                )
                user.set_password(password)
                user.save()
                request.session.set_expiry(604800)  # 1 week in seconds
                request.session.pop('registration', None)
                
                messages.success(request, "User registered successfully.")
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('users:otp_verification')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('users:otp_verification')

def login_view(request):
    if request.user.is_authenticated:
            raise Http404('you are already logged in !!!')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            mobile = form.cleaned_data.get('username')  # This will be the mobile
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=mobile, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.get_username() if user.get_username() else user.mobile}!")
                return redirect('redirect_url')
            else:
                messages.error(request, "Invalid mobile number or password")
        else:
            messages.error(request, "Invalid login details")
            return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})