from django.conf import settings

from .models import Request

from mwclient import Site
from mwclient.errors import APIError
from PIL import Image
import os
import re

pattern_request = re.compile(r'{{Request\s*\|\s*Name=([^|]+)\|\s*Email=([^|]+)\|\s*Message=([^}]+)}}')


def content_add_images(site, page, content):
    if page.image_dir is not None and os.path.exists(page.image_dir):
        for file in os.listdir(page.image_dir):
            filepath = os.path.join(page.image_dir, file)
            filename = f'Page_{page.pk}_image_{file}'

            # Upload image
            result = site.upload(open(filepath, 'rb'), filename)
            if result['result'] == 'Warning' and 'duplicate' in result['warnings']:
                filename = result['warnings']['duplicate'][0]

            # Get image width
            image = Image.open(filepath)
            width, height = image.size

            # Replace HTML tags with Wiki tags
            old_image_tag = fr'<img[^>]*src="{file}"[^>]*/>'

            width_option = '|800px' if width > 800 else ''
            new_image_tag = f'[[File:{filename}{width_option}]]'

            content = re.sub(old_image_tag, new_image_tag, content)

    return content


def delete_inner_links(content):
    count = 1
    while count > 0:
        # Sometimes there can be nested inner links:
        #   [[Link [[[[to]] content]]]]
        # Need to loop until there's nothing left
        content, count = re.subn(r'\[\[([^[\]]*)\[\[([^\]]+)]]([^\]]*)]]',
                                 r'[[\1\2\3]]',
                                 content)

    return content


def content_add_links(page, content):
    for link in page.link_set.filter(active=True):
        link_title = link.title
        # content = content.replace(link_title, f'[[{link_title}]]')
        content = content.replace(link_title, f'[[Special:FormEdit/Request/{link_title}|{link_title}]]')

    content = delete_inner_links(content)
    return content


def content_add_categories(page, content):
    categories = page.categories.all()

    if len(categories) > 0:
        content += "\n\n"

        for category in categories:
            content += f'[[Category:{category.name}]]'

    return content


def login_to_wiki():
    ua = 'WikiPA/0.1 (wikipa-bot@h2otoday.sausagemachine.net)'
    site = Site(settings.WIKI_URL, scheme='http', clients_useragent=ua, path='/')
    site.login(settings.WIKI_USERNAME, settings.WIKI_PASSWORD)

    return site


def push_to_wiki(page):
    site = login_to_wiki()

    content = page.content
    content = content_add_images(site, page, content)
    content = content_add_links(page, content)
    content = content_add_categories(page, content)

    wiki_page = site.pages[page.title]
    wiki_page.edit(content)

    # page.url = f'http://168.1.198.92/index.php/{wiki_page.name}'
    page.url = f'http://{settings.WIKI_URL}/wiki/{wiki_page.name}'
    page.save()


def delete_from_wiki(page):
    site = login_to_wiki()

    wiki_page = site.pages[page.title]

    try:
        wiki_page.delete()
    except APIError as e:
        if e.code == 'missingtitle':
            # The page doesn't exist, this is fine
            pass
        else:
            raise e


def scan_for_requests():
    site = login_to_wiki()
    for page in site.categories['Requests']:
        page_title = page.name

        request_exists = Request.objects.filter(page_title=page_title).count() != 0
        if not request_exists:
            page_text = page.text()
            match = pattern_request.search(page_text)

            if match is not None:
                expert_name = match.group(1).strip()
                expert_email = match.group(2).strip()
                message = match.group(3).strip()

                request = Request(page_title=page_title,
                                  expert_name=expert_name,
                                  expert_email=expert_email,
                                  message=message,
                                  )
                request.save()
