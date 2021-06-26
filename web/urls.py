from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('functioning/', views.functioning_view, name='functioning'),
    path('contactus/', views.contactus_view, name='contactus'),
    path('about/', views.about_view, name='about'),
    path('variability/', views.variability_view, name='variability_view'),
    path('bad_habits/', views.bad_habits_view, name='bad_habits_view'),
    path('create_csv_zip/<str:zip_name>/<str:rand_folder>/',
         views.create_csv_zip, name='create_csv_zip'),
    path('create_csv_student/<str:student>/', views.create_csv_student,
         name='create_csv_student'),
    path('create_csv_user/', views.create_csv_user, name='create_csv_user'),
    path('albums/upload/', views.upload_files_view, name='upload_files_view'),
    path('albums/upload_zip/', views.upload_file_zip_view,
         name='upload_file_zip_view'),
    path('analysis/<student>/<name_file>/', views.analysis_view,
         name='analysis_view'),
    path('analysis2/<student>/<project>/<file_name>/<rand_folder>/',
         views.analysis2_view, name='analysis2_view'),
    path('results/<file_name>/<mtime>/<type1>/<type2>/', views.results_view,
         name='results_view'),
    path('basedatos/', views.basedatos, name='basedatos'),
    path('review/', views.review_view, name='review_view'),
    path('students/<str:student>/', views.student_view, name='student_view'),
    path('delete/<str:student>/<str:file_name>/<str:times>/',
         views.delete_regist, name='delete_regist'),
    path('delete_student/<student>/', views.delete_student,
         name='delete_student'),
    path('edit_student/<old_student>/<new_student>/', views.edit_student,
         name='edit_student'),
    path('edit_file/<old_file>/<student>/<new_file>/', views.edit_file,
         name='edit_file'),
    path('settings/', views.settings_view, name='settings_view'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('accounts/login/', auth_views.LoginView.as_view(
            template_name='registration_web/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
            template_name='registration_web/logout.html'), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
            template_name='registration_web/password_change_form.html'),
         name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
            template_name='registration_web/password_change_done.html'),
         name='password_change_done'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(
            template_name='registration_web/password_reset_form.html'),
         name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
            template_name='registration_web/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='registration_web/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='registration_web/password_reset_complete.html'),
         name='password_reset_complete'),
    path('accounts/profile/', views.profile_view, name='profile'),
]
