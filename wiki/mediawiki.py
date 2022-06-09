from mwclient import Site


def content_add_links(page):
    content_with_links = page.content

    for link in page.link_set.filter(active=True):
        link_title = link.title
        content_with_links = content_with_links.replace(link_title,
                                                        f'[[{link_title}]]',
                                                        1)

    return content_with_links


def push_to_wiki(page):
    ua = 'Orchestrator/0.1 (orchestrator-bot@suasagemachine.org)'
    site = Site('localhost:8001', scheme='http', clients_useragent=ua, path='/')
    site.login('Admin', 'password12345!')
    pages = [p for p in site.pages]
    print(pages)
    for p in pages:
        print(p.name)

    content = content_add_links(page)
    page = site.pages[page.title]
    page.edit(content)
