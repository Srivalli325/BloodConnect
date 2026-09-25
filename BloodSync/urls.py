from django.contrib import admin
from django.urls import path
from BloodSync import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # =========================
    # AUTHENTICATION
    # =========================
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # =========================
    # HOME
    # =========================
    path('', views.home, name='home'),

    # =========================
    # DONOR
    # =========================
    path('add-donor/', views.add_donor, name='add_donor'),
    path('donors/', views.donor_list, name='donor_list'),
    path('update-donor/<int:id>/', views.update_donor, name='update_donor'),
    path('delete-donor/<int:id>/', views.delete_donor, name='delete_donor'),

    # =========================
    # BLOOD REQUEST
    # =========================
    path('blood-request/', views.blood_request_view, name='blood_request'),
    path('requests/', views.request_list, name='request_list'),
    path('update-request/<int:id>/', views.update_request, name='update_request'),
    path('delete-request/<int:id>/', views.delete_request, name='delete_request'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),
]