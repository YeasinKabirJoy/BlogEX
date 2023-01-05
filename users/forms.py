from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Skill,Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
        labels = {
            'first_name':'Name',
        }

    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm, self).__init__(*args,**kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({"class":"input"})


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','user_name','email','profile_picture','short_intro','description','location','social_github','social_linkedin','social_twitter','social_website']

    def __init__(self,*args,**kwargs):
        super(EditProfileForm, self).__init__(*args,**kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({"class":"input"})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self,*args,**kwargs):
        super(SkillForm, self).__init__(*args,**kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({"class":"input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name','email','subject','body']

    def __init__(self,*args,**kwargs):
        super(MessageForm, self).__init__(*args,**kwargs)

        for label,field in self.fields.items():
            field.widget.attrs.update({"class":"input"})