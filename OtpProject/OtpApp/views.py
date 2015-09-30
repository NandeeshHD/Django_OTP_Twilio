from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from forms import RegistrationForm, VerificationForm
from .models import User

# Create your views here.
def otp_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            if user.id:
                user.twiliosmsdevice_set.create(name='SMS', number=phone_number)
                device = user.twiliosmsdevice_set.get()
                device.generate_challenge()
            return HttpResponseRedirect('/otp/verify')
    else:
        form = RegistrationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('register.html', context)

def otp_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('next') != 'None':
                return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponse('User ' + user.username + ' is logged in.' +
                                '<p>Please <a href="/otp/status/">click here</a> to check verification status.</p>')
        else:
            return HttpResponse('User is invalid!' +
                                '<p>Please <a href="/otp/login/">click here</a> to login.</p>')
    else:
        form = AuthenticationForm()
    context = {}
    context['next'] = request.GET.get('next')
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('login.html', context)

@login_required(login_url='/otp/login')
def otp_verify(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        token = form.getToken()
        if token:
            user = User.objects.get_by_natural_key(request.user.username)
            device = user.twiliosmsdevice_set.get()
            #devices = django_otp.devices_for_user(user)
            if device:
                status = device.verify_token(token)
                print status
                if status:
                    user.is_verified = True
                    user.save()
                    return HttpResponse('User: ' + request.user.username + '\n' + 'Verified.' +
                                        '<p>Please <a href="/otp/logout/">click here</a> to logout.</p>')
                else:
                    return HttpResponse('User: ' + request.user.username + '\n' + 'could not be verified.' +
                                        '<p><a href="/otp/token/">Click here to generate new token</a></P>')
            else:
                return HttpResponse('User: ' + request.user.username + ' Worng token!' +
                                    '<p><a href="/otp/token/">Click here to generate new token</a></P>')
    else:
        form = VerificationForm()
    context = {}
    context.update(csrf(request))
    context['form'] = form
    return render_to_response('verify.html', context)

@login_required(login_url='/otp/login')
def otp_token(request):
    user = User.objects.get_by_natural_key(request.user.username)
    device = user.twiliosmsdevice_set.get()
    device.generate_challenge()
    return HttpResponseRedirect('/otp/verify')
    
def otp_status(request):
    if request.user.username:
        user = User.objects.get_by_natural_key(request.user.username)
        if user.is_verified:
            return HttpResponse(user.username + ' is verified.' +
                                '<p>Please <a href="/otp/logout/">click here</a> to logout.</p>')
        else:
            return HttpResponse(user.username + ' is not verified.' +
                                '<p><a href="/otp/token/">Click here to generate new token</a></P>')
    return HttpResponse('<p>Please <a href="/otp/login/">login</a> to check verification status.</p>')

def otp_logout(request):
    logout(request)
    return HttpResponse('You are logged out.' +
                        '<p>Please <a href="/otp/login/">click here</a> to login.</p>')
