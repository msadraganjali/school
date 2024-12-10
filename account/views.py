from typing import Any, Dict
from django.forms.models import BaseModelForm
from . import forms
from .mixins import *
from .forms import SignupForm
from blog.models import Article
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import User, Form_Registeration, Reserve
from extensions.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from melipayamak.melipayamak import Api as MelipayamakApi
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Create your views here.

class RegFormCreateForm(RegFormValidMixin, RegFieldsMixin, CreateView):
    model = Form_Registeration
    template_name = 'registration/reg.html'

class ArticleList(AuthorsAccessMixin, ListView):
	template_name = "registration/home.html"

	def get_queryset(self):
		if self.request.user.is_superuser:
			return Article.objects.all()
		else:
			return Article.objects.filter(author=self.request.user)


class ReserveListView(ListView):
    template_name = 'registration/reserve.html'
    queryset = Reserve.objects.all().order_by('datetime')

    
def ReserveListViewForm(request, reserve_id):
    reserve_list = Reserve.objects.all().order_by('datetime', 'user')
    if request.method == 'POST':
        form = forms.ReserveSendStatusFormClass(request.POST)
        if not form.is_valid() or form.is_valid():
            userReserves = Reserve.objects.filter(user = request.user)
            if not userReserves:
                reserve_obj = Reserve.objects.filter(id = reserve_id)
                reserve_obj.update(user = request.user)
            else:
                return render(request , 'registration/reserve.html' , {'form' : form, 'object_list' : reserve_list, 'alert' : 'false'})  
                
    else:
       form = forms.ReserveSendStatusFormClass()

    return render(request , 'registration/reserve.html' , {'form' : form, 'object_list' : reserve_list, 'alert' : 'true'})  


# Article CRUD

class ArticleCreate(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
	model = Article
	template_name = "registration/article-create-update.html"


class ArticleUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
	model = Article
	template_name = "registration/article-create-update.html"


class ArticleDelete(SuperUserAccessMixin, DeleteView):
	model = Article
	success_url = reverse_lazy('auth:home')
	template_name = "registration/article_confirm_delete.html"

# Authenctication System Forms

class Profile(LoginRequiredMixin ,UpdateView):
	model = User
	template_name = "registration/profile.html"
	form_class = forms.ProfileForm
	success_url = reverse_lazy("auth:profile")

	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)

	def get_form_kwargs(self):
		kwargs = super(Profile, self).get_form_kwargs()
		kwargs.update({
			'user': self.request.user
		})
		return kwargs

class Login(LoginView):
	def get_success_url(self):
		user = self.request.user

		if user.is_superuser or user.is_author:
			return reverse_lazy("auth:home")
		else:
			return reverse_lazy("auth:profile")

class Logout(LogoutView):
    def get_success_url(self):
        logout(self.request)
        return reverse_lazy('login')

class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال‌سازی اکانت'
        message = render_to_string('registration/activate.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        # to_email = form.cleaned_data.get('email')
        to_email = "sadraganjali@gmail.com"
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        username = settings.MELIPAYAMAK['USERNAME']
        password = settings.MELIPAYAMAK['PASSWORD']
        _from = settings.MELIPAYAMAK['FROM']
        sms_to = form.cleaned_data.get('phone')
        description = render_to_string('registration/activate.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
		})
        api = MelipayamakApi(username,password)
        sms = api.sms()
        response = sms.send(sms_to,_from,description)
        return render(self.request, 'registration/done.html')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/account-active.html')
    else:
        return render(request, 'registration/account-not-active.html')