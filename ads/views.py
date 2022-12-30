import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ads.models import Ads, Categories


def get_base_url(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        ads = Ads.objects.all()
        response = [{"id": ad.pk,
                     "name": ad.name,
                     "author": ad.author,
                     "price": ad.price} for ad in ads]
        return JsonResponse(response, safe=False)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ads()
        ad.name = ad_data['name']
        ad.author = ad_data['author']
        ad.price = ad_data['price']
        ad.description = ad_data['description']
        ad.address = ad_data['address']
        ad.is_published = ad_data['is_published']

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        ad.save()
        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


class AdsEntityView(View):
    def get(self, request, pk):
        ad = get_object_or_404(Ads, id=pk)

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
class CategoriesView(View):
    def get(self, request):
        cats = Categories.objects.all()
        response = [{"id": cat.pk,
                     "name": cat.name} for cat in cats]
        return JsonResponse(response, safe=False)

    def post(self, request):
        cat_data = json.loads(request.body)

        cat = Categories()
        cat.name = cat_data['name']

        try:
            cat.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        cat.save()
        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        })


class CategoriesEntityView(View):
    def get(self, request, pk):
        cat = get_object_or_404(Categories, id=pk)

        return JsonResponse({
            "id": cat.pk,
            "name": cat.name
        })
