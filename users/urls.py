from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("dropbox_auth/",views.dropbox_auth,name="dropbox_auth"),
    path("dropbox/",views.dropbox,name="dropbox"),

    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("register/",views.register_user,name="register"),


    path("", views.profiles, name="profiles"),
    path("profile/<str:id>", views.user_profile, name="user-profile"),
    path("account/", views.account, name="account"),
    path("edit-profile/", views.edit_profile, name="edit-profile"),
    path("inbox/", views.inbox, name="inbox"),
    path("message/<str:id>/", views.read_message, name="message"),
    path("send-message/<str:id>/", views.create_message, name="send-message"),


    path("add-skill", views.add_skill, name="add-skill"),
    path("update-skill/<str:id>/", views.update_skill, name="update-skill"),
    path("delete-skill/<str:id>/", views.delete_skill, name="delete-skill"),

    path('change-password/', auth_views.PasswordChangeView.as_view(
            template_name='users/change-password.html'), name='change_password'),
    path('change-password-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/change-password-done.html'), name='password_change_done'),


    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='users/reset-password.html'), name='password_reset'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
       template_name='users/reset-password-sent.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/reset-password-page.html'), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/reset-password-complete.html'), name='password_reset_complete')




]