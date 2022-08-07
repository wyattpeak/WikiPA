from mwclient import Site
import os
import re


def content_add_images(site, page, content):
    if page.image_dir is not None and os.path.exists(page.image_dir):
        for file in os.listdir(page.image_dir):
            filepath = os.path.join(page.image_dir, file)
            filename = f'Page_{page.pk}_image_{file}'

            print(filename)
            result = site.upload(open(filepath, 'rb'), filename)
            print(result)

            if result['result'] == 'Warning' and 'duplicate' in result['warnings']:
                filename = result['warnings']['duplicate'][0]
                print(f'Duplicate: {filename}')

            old_image_tag = f'<img src="{file}" />'
            new_image_tag = f'[[File:{filename}]]'

            content = content.replace(old_image_tag, new_image_tag)

    return content


def delete_inner_links(content):
    content = re.sub(r'\[\[([^[\]]*)\[\[([^\]]+)]]([^\]]*)]]',
                     r'[[\1\2\3]]',
                     content)

    return content


def content_add_links(page, content):
    for link in page.link_set.filter(active=True):
        link_title = link.title
        content = content.replace(link_title, f'[[{link_title}]]')

    content = delete_inner_links(content)
    return content


def push_to_wiki(page):
    ua = 'Orchestrator/0.1 (orchestrator-bot@suasagemachine.org)'
    site = Site('168.1.198.92', scheme='http', clients_useragent=ua, path='/')
    site.login('Admin', 'password12345!')

    # content = content_add_images(site, page)

    content = page.content
    content = content_add_images(site, page, content)
    content = content_add_links(page, content)

    wiki_page = site.pages[page.title]
    wiki_page.edit(content)

    page.url = f'http://168.1.198.92/index.php/{wiki_page.name}'
    page.save()
