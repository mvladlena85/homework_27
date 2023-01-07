import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from ads.models import Ads, Categories


def get_base_url(request):
    return JsonResponse({"status": "ok"})


class AdsView(ListView):
    model = Ads
    queryset = Ads.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = [{"id": ad.pk,
                     "name": ad.name,
                     "author": ad.author,
                     "price": ad.price} for ad in self.object_list]
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'address', 'is_published']

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ads.objects.create(name=ad_data['name'],
                                author=ad_data['author'],
                                price=ad_data['price'],
                                description=ad_data['description'],
                                address=ad_data['address'],
                                is_published=ad_data['is_published'])

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'address']

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ads.objects.create(name=ad_data['name'],
                                author=ad_data['author'],
                                price=ad_data['price'],
                                description=ad_data['description'],
                                address=ad_data['address'],
                                is_published=ad_data['is_published'])

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


class AdsEntityView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "address": self.object.address,
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