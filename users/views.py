from django.http import Http404, JsonResponse
from django.shortcuts import render,redirect
from .models import Profile,Skill
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm,EditProfileForm,SkillForm,MessageForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .utils import search_profile,paginate_profiles
import requests
from django.utils.safestring import mark_safe
# Create your views here.


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            return redirect('login')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Username OR password is invalid")
            return redirect('login')
    context={
        'page':page
    }
    return render(request,'users/login-register.html',context)

@login_required(login_url='login')
def logout_user(request):
    messages.info(request, "User was logged out!")
    logout(request)
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            try:
                User.objects.get(username=user.username)
                messages.error(request,'Username Already Exists')
                form = CustomUserCreationForm(request.POST)
                context = {
                    'page': page,
                    'form': form
                }
                return render(request,'users/login-register.html', context)
            except ObjectDoesNotExist:
                user.save()
                messages.success(request,'Add a Short Intro and Description for you account to show up to other blogger')
                login(request,user)
                return redirect('edit-profile')
        else:
            messages.error(request,'An error has occurred during registration')
    context={
        'page':page,
        'form':form
    }
    return render(request,'users/login-register.html',context)



def profiles(request):
    all_profile,search_text = search_profile(request)
    all_profile,custom_range = paginate_profiles(request,all_profile,6)
    context={
        "profiles":all_profile,
        "search_text":search_text,
        'custom_range':custom_range
    }
    return render(request,'users/profiles.html',context)


def user_profile(request,id):
    profile= Profile.objects.get(id=id)
    top_skill = profile.skill_set.exclude(description__exact="")
    other_skill = profile.skill_set.filter(description="")

    context={
        "profile":profile,
        "top_skill":top_skill,
        "other_skill":other_skill
    }
    return render(request,'users/user-profile.html',context)


@login_required(login_url='login')
def account(request):
    profile = request.user.profile
    context={
        'profile':profile,
    }
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    form = EditProfileForm(instance=profile)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updated')
            return redirect('account')
    context = {
        'form':form,
    }

    return render(request,'users/profile-form.html',context)


@login_required(login_url='login')
def add_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill Added')
            return redirect('account')

    context ={
         'form':form
    }

    return render(request,'users/skill-form.html',context)


@login_required(login_url='login')
def update_skill(request,id):
    profile = request.user.profile

    try:
        skill = profile.skill_set.get(id=id)
    except ObjectDoesNotExist:
        raise Http404

    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill Updated')
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def delete_skill(request, id):

    profile = request.user.profile
    try:
        skill = profile.skill_set.get(id=id)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == "POST":
        skill.delete()
        return redirect('account')
    context={
        'object':skill.name
    }
    return render(request,"delete-object.html",context)


def inbox(request):
    profile = request.user.profile
    all_messages = profile.messages.all()
    unread_messages_count = all_messages.filter(is_read=False).count()

    context={
        'all_messages':all_messages,
        'unread_messages_count':unread_messages_count
    }
    return render(request,'users/inbox.html',context)


def read_message(request,id):
    profile = request.user.profile
    message = profile.messages.get(id=id)

    if not message.is_read:
        message.is_read = True
        message.save()

    context={
        'message':message
    }
    return render(request,'users/message.html',context)


def create_message(request,id):
    recipient = Profile.objects.get(id=id)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request,"Your message was successfully sent")
            return redirect('user-profile',id=recipient.id)
    context={
        'recipient':recipient,
        'form':form
    }

    return render(request,'users/message-form.html',context)


DROPBOX_KEY = ""
DROPBOX_SECRET = ""


def dropbox_auth(request):
    return redirect("https://www.dropbox.com/oauth2/authorize?client_id=hc8zt24chpujhnd&redirect_uri=http://127.0.0.1:8000/dropbox/&response_type=code&token_access_type=offline")


def dropbox(request):
    code = request.GET["code"]
    data = requests.post("https://api.dropboxapi.com/oauth2/token",data={
        "code":code,
        "grant_type":"authorization_code",
        "redirect_uri":"http://127.0.0.1:8000/dropbox/"

    },auth=(DROPBOX_KEY,DROPBOX_SECRET))

    return JsonResponse(data.json())
