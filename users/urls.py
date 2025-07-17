from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register_view, RegisterView, OTPVerificationView, login_view,user_list,create_user,update_user,delete_user,bulk_upload_users

app_name='users'
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    # path('register/', register_view, name="register"),
    path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
    path('verify/', OTPVerificationView.as_view(), name='otp_verification'),
    path('users/', user_list, name='user_list'),
    path('users-create/', create_user, name='create_user'),
    path('users/update/<int:pk>/', update_user, name='update_user'),
    path('users/delete/<int:pk>/', delete_user, name='delete_user'),
    path('users/bulk-upload/', bulk_upload_users, name='bulk_upload_users'),
]
