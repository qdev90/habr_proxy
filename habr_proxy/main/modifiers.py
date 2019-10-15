"""
Modifiers
All modifiers must be inherited from Base modifier.
"""
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from django.conf import settings


class BaseModifier(object):
    @staticmethod
    def modify_html(html, request):
        """
        Returns modified html

        html: string
        request: django HttpRequest
        """
        raise NotImplementedError


class URLModifier(BaseModifier):
    """
    Replace host URLs inside the <a> and <use> tags.
    Example:
        <a href='https://habr.com/ru/yandex/post/432562/' ...> will be replaced
        with <a href='http://localhost:8000/ru/yandex/post/432562/' ...>
    """
    @staticmethod
    def modify_html(html, request):
        soup = BeautifulSoup(html, 'html5lib')
        host_url = request.build_absolute_uri('/')
        link_pattern = r'^{}(.*)'.format(settings.TARGET_SITE)

        for tag in soup.find_all('a', href=re.compile(link_pattern)):
            tag['href'] = re.sub(
                link_pattern,
                r'{}\1'.format(host_url),
                tag['href']
            )

        # tags 'use' have specific attribute 'xlink:href'
        for tag in soup.find_all('use'):
            tag['xlink:href'] = re.sub(
                link_pattern,
                r'{}\1'.format(host_url),
                tag['xlink:href']
            )

        return str(soup)


class SixLettersWordsModifier(BaseModifier):
    """
    Extends words of 6 length with symbol ™ in the text.
    """
    @staticmethod
    def modify_html(html, request):
        soup = BeautifulSoup(html, 'html5lib')
        pattern = r'\b(\w{6})\b'

        # find all text inside tags
        def has_content(tag):
            return any(bool(re.search(pattern, content))
                       for content in tag.contents
                       if isinstance(content, NavigableString))

        # modify each text instance inside tags
        for tag in soup.body.find_all(has_content):
            for content in tag.contents:
                if isinstance(content, NavigableString):
                    new_content = NavigableString(
                        re.sub(
                            pattern,
                            r'\1™',
                            content
                        )
                    )
                    content.replace_with(new_content)

        return str(soup)
