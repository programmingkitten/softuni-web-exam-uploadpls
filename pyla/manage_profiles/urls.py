from django.urls import path
from django.views.generic import TemplateView

from pyla.manage_profiles.views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileView
from pyla.manage_profiles.views import ProfileEditView
urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout', UserLogoutView.as_view(), name='logout user'),
    path('completed-registraion/', TemplateView.as_view(template_name="manage_profiles/auth/successful_register.html"),
         name='registered successfully'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile view'),
    path('edit-profile/<int:pk>', ProfileEditView.as_view(), name='edit profile'),
]
