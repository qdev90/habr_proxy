import requests
from urllib.parse import urljoin
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from .modifiers import URLModifier
from .modifiers import SixLettersWordsModifier


class SiteProxyView(View):
    """
    Receives page from habr.com/<full_path> and returns modified page.
    <full_path> extracted from request.
    All modifiers located inside main.modifiers.
    Change MODIFIERS list to enable/disable modifiers.
    """
    # List of modifiers to use
    MODIFIERS = [
        URLModifier,
        SixLettersWordsModifier,
    ]

    def get(self, request):
        full_path = request.get_full_path()
        response = requests.get(urljoin(settings.TARGET_SITE, full_path))
        modified_content = response.content
        if 'text/html' in response.headers['Content-Type']:
            for modifier in self.MODIFIERS:
                modified_content = modifier.modify_html(modified_content, request)
        return HttpResponse(modified_content, content_type=response.headers['Content-Type'])
