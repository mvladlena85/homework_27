from django.urls import path

from users import views

urlpatterns = [
    path("", views.UsersView.as_view(), name="user_list"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user_detail_info"),
    path("create/", views.UserCreateView.as_view(), name="create_user"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="update_user"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete_user"),
    ]
