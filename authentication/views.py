from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib import auth
from validate_email import validate_email


# Create your views here.

class ResgistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):
        #get user data:
        #validate
        #create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues' : request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,'Password too short')
                    return render(request,'authentication/register.html',context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                # email_subject = 'Activate your account'
                # email_body = 'Test message'
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@cashflow.com',
                #     [email],
                # )

                # email.send(fail_silently=False)
                messages.success(request,'Account successfully created!')
                return render(request,'authentication/register.html')

        return render(request,'authentication/register.html')
    

class UserNameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error' : 'username should only contain alphanumeric characters'}, status=400)
    
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error' : 'sorry username in use, please choose another one'}, status=409)
        

        return JsonResponse({'username_valid' : True})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email=data['email']

        if not validate_email(email):
            return JsonResponse({'email_error' : 'Email is invalid'}, status=400)
    
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error' : 'sorry email in use, please choose another one'}, status=409)
        

        return JsonResponse({'email_valid' : True})
    

class LoginView(View):
    def loginuser(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password') 
            #check if the user has correct credentials: 
            user = authenticate(username=username, password=password)
            if user is not None:
            # A backend authenticated the credentials
                login(request, user)
                return redirect("/")
        
            else:
            # No backend authenticated the credentials
                messages.warning(request, "Incorrect Credentials!")
                return render(request, "login.html")

        return render(request, "login.html")