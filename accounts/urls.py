
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path("user/", views.specific_user_view),
    re_path("signin", views.sign_view),
    re_path("", views.users_view, name="users view 1")
]
