from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

# app_name = "users"

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activation'),
    path('login/', views.Login.as_view(), name='login'),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="user/password_reset.html",
                                                                 email_template_name='user/password_reset_email.html'), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="user/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>",
         auth_views.PasswordResetConfirmView.as_view(template_name="user/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="user/password_reset_complete.html"), name="password_reset_complete"),
]
