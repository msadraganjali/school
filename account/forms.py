from django import forms
from .models import User, Reserve
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user')
        
        super(ProfileForm, self).__init__(*args, **kwargs)
    
        self.fields['username'].help_text = False
        if user.is_superuser or user.is_staff:
            self.fields['username'].disabled = False
            # self.fields['email'].disabled = False
            self.fields['phone'].disabled = False
            self.fields['is_author'].disabled = False
            self.fields['special_user'].disabled = False
        else:
            self.fields['username'].disabled = True
            # self.fields['email'].disabled = True
            self.fields['phone'].disabled = True
            self.fields['is_author'].disabled = True
            self.fields['special_user'].disabled = True
            
    
    class Meta:
        model = User
        # fields = ["username", "email", "first_name", "last_name", "special_user", "is_author"]
        fields = ["username", "phone", "first_name", "last_name", "special_user", "is_author"]

class SignupForm(UserCreationForm):
    phone = forms.CharField(max_length=11)
    class Meta:
        model = User
        # fields = ('username', 'email', 'password1', 'password2')
        fields = ('username', 'phone', 'password1', 'password2')

class ReserveSendStatusFormClass(forms.Form):
    class Meta:
        model = Reserve
        fields = ["user", "datetime"]