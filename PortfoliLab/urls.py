from django.contrib import admin
from django.urls import path
from clothesresourcing_app.views import LandingPageView, AddDonationView, LoginView, RegisterView,\
    LogoutView, get_institution_by_category, ProfilView, ConfirmationView, FormSaveView, ProfileSettingsView, MessageTestView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_donation/', AddDonationView.as_view(), name='add-donation'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfilView.as_view(), name='profil'),
    path('get_institution_by_category/', get_institution_by_category, name='get-institution-by-category'),
    path('save/', FormSaveView.as_view(), name='form-save'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('settings/', ProfileSettingsView.as_view(), name='settings'),
    path('message', MessageTestView.as_view(), name='message')

]
