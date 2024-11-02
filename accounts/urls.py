from django.urls import path

from .services import activate_account, block_account, unlock_account
from .views import register_view, accounts_list, CustomUserDetailView, CustomUserEditView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('accounts/', accounts_list, name='accounts'),
    path('accounts/<int:pk>/', CustomUserDetailView.as_view(), name='user_detail'),
    path('accounts/<int:pk>/edit', CustomUserEditView.as_view(), name='user_edit'),
    path('accounts/<int:user_id>/block', block_account, name='block_account'),
    path('accounts/<int:user_id>/unlock', unlock_account, name='unlock_account'),
]
