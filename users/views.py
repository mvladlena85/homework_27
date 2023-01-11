import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ads
from homework_27 import settings
from users.models import User, Location


class UsersView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.annotate(ads_number=Count('ads', filter=Q(ads__is_published=True))).
                              prefetch_related('location_id'), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        response = {
            "items": [{
                "id": user.pk,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.location_id.all())),
                "total_ads": user.ads_number
            } for user in page_obj],
            "total": paginator.count,
            "num_pages": paginator.num_pages
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, *args, **kwargs)

        response = {"id": user.pk,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    "locations": list(map(str, user.location_id.all()))}

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(username=user_data['username'],
                                   password=user_data['password'],
                                   first_name=user_data['first_name'],
                                   last_name=user_data['last_name'],
                                   role=user_data['role'],
                                   age=user_data['age'],
                                   )
        locations = user_data['locations']

        for location in locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location_id.add(location_obj)

        user.save()

        response = {"id": user.pk,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                    "age": user.age,
                    "locations": list(map(str, user.location_id.all()))}

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age"]

    def patch(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        super().post(request, *args, **kwargs)

        if 'username' in user_data:
            self.object.username = user_data['username']
        if 'password' in user_data:
            self.object.password = user_data['password']
        if 'first_name' in user_data:
            self.object.first_name = user_data['first_name']
        if 'last_name' in user_data:
            self.object.last_name = user_data['last_name']
        if 'role' in user_data:
            self.object.role = user_data['role']
        if 'age' in user_data:
            self.object.age = user_data['age']

        if 'locations' in user_data:
            locations = user_data['locations']
            self.object.location_id.all().delete()

            for location in locations:
                location_obj, _ = Location.objects.get_or_create(name=location)
                self.object.location_id.add(location_obj)

        self.object.save()

        response = {"id": self.object.pk,
                    "username": self.object.username,
                    "first_name": self.object.first_name,
                    "last_name": self.object.last_name,
                    "role": self.object.role,
                    "age": self.object.age,
                    "locations": list(map(str, self.object.location_id.all()))}

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
