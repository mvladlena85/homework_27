from django.urls import path

from ads import views

urlpatterns = [
    path("", views.get_base_url, name="base"),
    path("ad/", views.AdsView.as_view(), name="ads"),
    path("ad/<int:pk>", views.AdsEntityView.as_view(), name="full_ad"),
    path("cat/", views.CategoriesView.as_view(), name="categories"),
    path("cat/<int:pk>", views.CategoriesEntityView.as_view(), name="category"),
    ]
