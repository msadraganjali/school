from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article

class FieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
			"title", "slug", "category",
			"description", "thumbnail", "publish",
			"is_special", "status",
		]
		if request.user.is_superuser:
			self.fields.append("author")
		return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
	def form_valid(self, form):
		if self.request.user.is_superuser:
			form.save()
		else:
			self.obj = form.save(commit=False)
			self.obj.author = self.request.user
			if not self.obj.status == 'i':
				self.obj.status = 'd'
		return super().form_valid(form)


class AuthorAccessMixin():
	def dispatch(self, request, pk, *args, **kwargs):
		article = get_object_or_404(Article, pk=pk)
		if article.author == request.user and article.status in ['b', 'd'] or\
		request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")


class AuthorsAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_superuser or request.user.is_author:
				return super().dispatch(request, *args, **kwargs)
			else:
				return redirect("auth:profile")
		else:
			return redirect("login")


class SuperUserAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")


class RegFieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = ['type', 'name', 'lastname', 'father_name', 'nid', 'creation_certificate', 'birth_localtion', 'date_of_birth_day', 'the_name_of_privous_school', 'religion', 'religion_of_religion', 'student_parent', 'father_first_name', 'father_last_name', 'father_date_of_birth_day', 'level_of_education_father', 'job_father', 'telephone_number_work_location_father', 'work_location_adderss_father', 'father_phone_number', 'father_live', 'mother_first_name', 'mother_last_name', 'mother_date_of_birth_day', 'level_of_education_mother', 'job_mother', 'telephone_number_work_location_mother', 'work_location_adderss_mother', 'mother_phone_number', 'mother_live', 'ghaim_first_name', 'ghaim_last_name', 'ghaim_date_of_birth_day', 'level_of_education_ghaim', 'job_ghaim', 'telephone_number_work_location_ghaim', 'work_location_adderss_ghaim', 'ghaim_phone_number', 'street', 'alley', 'alley_alley', 'plaque', 'floor', 'postal_code', 'telephone_number', 'number_of_shad', 'emergensy_phone']
		return super().dispatch(request, *args, **kwargs)


class RegFormValidMixin():
	def form_valid(self, form):
		self.obj = form.save(commit=False)
		self.obj.user = self.request.user
		return super().form_valid(form)