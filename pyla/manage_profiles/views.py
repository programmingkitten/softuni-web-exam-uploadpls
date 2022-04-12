import django.views.generic as views
from django.contrib.auth import forms as auth_forms, get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from pyla.manage_profiles.forms import ProfileForm, CreateFeedbackForm
from pyla.manage_profiles.mixins import CRUDAccessMixin, FullCRUDProfileMixin
from pyla.manage_profiles.models import Profile, ContactUs

UserModel = get_user_model()


# will only show the template if the user is logged in. Good for forum posts

class UserRegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'nickname',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(

            user=user,
        )

        if commit:
            profile.save()
        return user


class UserRegistrationView(views.CreateView):
    # form_class = auth_forms.UserCreationForm
    form_class = UserRegistrationForm
    template_name = 'manage_profiles/auth/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'manage_profiles/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):

    def get_next_page(self):
        return reverse_lazy('index')


class FormView(ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'moto', 'profile_picture')


class ProfileView(LoginRequiredMixin, views.DetailView):
    template_name = 'manage_profiles/user/profile.html'
    model = Profile
    user = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.pk == self.kwargs['pk']:
            context['CRUD_ACCESS'] = True
            # if True instead of "Edit" button there will be "Add friend" button.
        return context


class ProfileEditView(LoginRequiredMixin, FullCRUDProfileMixin, views.UpdateView): # TESTED
    template_name = 'manage_profiles/user/edit-profile.html'
    model = Profile
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('index')

