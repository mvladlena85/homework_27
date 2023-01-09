import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from ads.models import Ads, Categories
from users.models import User


def get_base_url(request):
    return JsonResponse({"status": "ok"})


class AdsView(ListView):
    model = Ads
    queryset = Ads.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = [{"id": ad.pk,
                     "name": ad.name,
                     "author_id": ad.author.pk,
                     "price": ad.price,
                     "category_id": ad.category.pk} for ad in self.object_list]
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ads.objects.create(name=ad_data['name'],
                                author=get_object_or_404(User, pk=ad_data['author_id']),
                                price=ad_data['price'],
                                description=ad_data['description'],
                                is_published=ad_data['is_published'],
                                category=get_object_or_404(Categories, pk=ad_data['category_id']),
                                )

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author_id": ad.author.pk,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "category_id": ad.category.pk,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request):
        ad_data = json.loads(request.body)

        self.object.name = ad_data['name']
        self.object.author = ad_data['author_id']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.category = ad_data['category_id']

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author_id": self.object.author.pk,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "category_id": self.object.category.pk,
            "image": self.object.image.url if self.object.image else None,
            "is_published": self.object.is_published
        })


class AdsEntityView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
            "is_published": self.object.is_published
        })


class AdsDeleteView(DeleteView):
    model = Ads

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category', 'image']

    def post(self, request, *args, **kwargs):
        self.object = super().get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "category": self.object.category.name,
            "image": self.object.image.url if self.object.image else None,
            "is_published": self.object.is_published
        })



class CategoriesView(ListView):
    model = Categories
    queryset = Categories.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = [{"id": cat.pk,
                     "name": cat.name} for cat in self.object_list]
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)

        cat = Categories.objects.create(name=cat_data['name'])
        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        super().post(request, *args, **kwargs)

        self.object.name = cat_data['name']

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name
        })


class CategoriesEntityView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        cat = get_object_or_404(Categories, *args, **kwargs)

        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        })


class CategoryDeleteView(DeleteView):
    model = Categories

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
