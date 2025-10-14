from django.urls import path

from account.views import forgot_password, register_user, login_user, logout_admin, profile, verify_phone, resend_code

app_name = "account"

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_admin, name='logout'),
    path('register/', register_user, name='register'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('profile/', profile, name='profile'),
    path('verify_phone/', verify_phone, name='verify_phone'),
    path('resend_code/', resend_code, name='resend_code'),

    # path('success_confrimed/<custom_user_id>/<int:code_send>/', ConfrimUserSuccessView.as_view(), name='Confrim_User_success'),

    # path('ResentCode/<custom_user_id>/', ResentCode.as_view(), name='resent_code'),
    # path('confrimed_user_success', Confrim_User_success, name='Confrim_User_success'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
