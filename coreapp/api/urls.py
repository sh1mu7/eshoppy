from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'country', views.CountryAPI)

urlpatterns = [
    path('signup/', views.SignupAPI.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('delete/', views.DeleteAccountAPI.as_view(), name='delete-account'),
    path('user/', include('coreapp.api.admin.urls')),
    path('profile/', views.ProfileAPI.as_view(), name='profile'),
    path('verification/resend/', views.ResendVerificationAPI.as_view(), name='resend-verification'),
    path('verification/check/', views.OTPCheckAPI.as_view(), name='otp-check'),
    path('account/verify/', views.AccountVerifyAPI.as_view(), name='account-verify'),
    path('change/password/', views.PasswordChangeAPI.as_view(), name='change-password'),
    path('forget/password/', views.ForgetPasswordAPI.as_view(), name='forget-password'),
    path('forget/password/confirm/', views.ForgetPasswordConfirmAPI.as_view(), name='forget-password-confirm'),
    path('documents/upload/', views.UploadDocumentsAPI.as_view(), name='forget-password-confirm'),
]
urlpatterns += router.urls
