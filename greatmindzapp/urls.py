from django.urls import path
from . import views
from .views import BlogDetailView, BlogListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('become-a-tutor/', views.becomeatutor, name='becomeatutor'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('getatutor/', views.getatutor, name='getatutor'),
    path('tutorapplication/', views.tutorapplication, name='tutorapplication'),
    path('all_tutors/', views.alltutors, name='alltutors'),
    path('login/', views.login_view, name='login'),

    path('confirm-email/<confirmation_token>', views.confirmEmail, name='confirm_email'),
    #path('activate/<uidb64>/token>', views.activate, name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('logout/', views.logout_view, name='logout'),
    path('myjobs/', views.myjobs, name = 'myjobs'),
    path('available_jobs/<int:pk>/', views.apply_job, name='apply_job'),
    path('view-profile/<int:id>/', views.view_profile, name='view-profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('current-applications', views.current_applications, name = 'current_applications'),
    path('current-jobs', views.current_jobs, name = 'current_jobs'),
    path('dashboard', views.dashboard, name = 'dashboard'),  

    path('available_jobs/', views.available_jobs, name='available_jobs'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_single'),
    path('terms-and-conditions/', views.terms, name="terms"),
    path('privacy-policy/', views.privacy, name="privacy_policy"),
    path('client-terms-and-/', views.client_terms, name="client_terms"),
    path('tutor-terms-and-conditions/', views.tutor_terms, name="tutor_terms"),
    path('tutors-by-subject/<int:id>/<str:is_online>/', views.tutors_by_subject, name="tutors_by_subject"),
    path('life-sciences-tutors/', views.life_sciences_tutors, name="life_sciences_tutors"),
    path('payment/', views.payment_info, name='payment_info'),


    
]