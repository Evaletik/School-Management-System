from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile('auth/login'), compile('admin/login')]

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(reverse('login'))
        response = self.get_response(request)
        return response