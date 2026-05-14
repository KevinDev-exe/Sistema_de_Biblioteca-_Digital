from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    path(
        'registro/',
        views.registro,
        name='registro'
    ),

    path(
        'perfil/',
        views.perfil,
        name='perfil'
    ),

    path(
        'usuarios/',
        views.usuarios,
        name='usuarios'
    ),

    path(
        'editar-usuario/<int:user_id>/',
        views.editar_usuario,
        name='editar_usuario'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
    'password-reset/',
    views.password_reset_view,
    name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    path(
    'dashboard/',
    views.dashboard,
    name='dashboard'
),
]