from django.urls import path

from ads import views

urlpatterns = [
    path("", views.get_base_url, name="base"),
    path("ad/", views.AdsView.as_view(), name="ads"),
    path("ad/create/", views.AdsCreateView.as_view(), name="create_ad"),
    path("ad/<int:pk>/", views.AdsEntityView.as_view(), name="full_ad"),
    path("ad/<int:pk>/update/", views.AdsUpdateView.as_view(), name="update_ad"),
    path("ad/<int:pk>/delete/", views.AdsDeleteView.as_view(), name="delete_ad"),
    path('ad/<int:pk>/upload_image/', views.AdsImageView.as_view(), name="upload_image"),
    path("cat/", views.CategoriesView.as_view(), name="categories"),
    path("cat/create/", views.CategoryCreateView.as_view(), name="create_category"),
    path("cat/<int:pk>", views.CategoriesEntityView.as_view(), name="category"),
    path("cat/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="update_category"),
    path("cat/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="delete_category"),
    ]
