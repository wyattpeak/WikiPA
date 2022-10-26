from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormView
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from pathlib import Path
import re

from .models import Page, Category, Request
from .forms import PageForm, PageBulkImportForm, BackupLoadForm, CategoryForm
from .mediawiki import push_to_wiki, scan_for_requests
from .sendgrid import send_request_emails
from .backup import dump

pattern_page_title = re.compile(r'You were nominated as an expert on "(.+?)".')


def index(request):
    return redirect('wiki:page-index')


class PageListView(ListView):
    model = Page
    template_name = 'wiki/page/index.html'
    context_object_name = 'page'
    paginate_by = 10


class PageCreateView(FormView):
    form_class = PageForm
    template_name = 'wiki/page/create.html'
    success_url = reverse_lazy('wiki:page-index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PageDeleteView(DeleteView):
    model = Page
    template_name = 'wiki/page/delete.html'
    success_url = reverse_lazy('wiki:page-index')


def page_push(request, pk):
    page = get_object_or_404(Page, pk=pk)
    links = page.link_set.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        active_links = [int(pk) for pk in request.POST.getlist('link[]')]

        for link in links:
            link.active = (link.pk in active_links)
            link.save()

        active_categories = [int(pk) for pk in request.POST.getlist('category[]')]

        for category in categories:
            if category.pk in active_categories:
                page.categories.add(category)
            else:
                page.categories.remove(category)

        push_to_wiki(page)

    # We grab this here because it may have been updated by the POST section
    page_categories = page.categories.all()

    context = {
        'page': page,
        'links': links,
        'categories': categories,
        'page_categories': page_categories
    }

    return render(request, 'wiki/page/push.html', context)


class PageBulkImportView(FormView):
    form_class = PageBulkImportForm
    template_name = 'wiki/page/bulk-import.html'
    success_url = reverse_lazy('wiki:page-index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def backup_dump(request):
    dump_bytes = dump()
    response = HttpResponse(dump_bytes, content_type="application/gzip")
    response['Content-Disposition'] = 'inline; filename=backup.tgz'
    return response


class BackupLoadView(FormView):
    form_class = BackupLoadForm
    template_name = 'wiki/backup-load.html'
    success_url = reverse_lazy('wiki:page-index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CategoryListView(ListView):
    model = Category
    template_name = 'wiki/category/index.html'
    context_object_name = 'category'
    paginate_by = 10


class CategoryCreateView(FormView):
    form_class = CategoryForm
    template_name = 'wiki/category/create.html'
    success_url = reverse_lazy('wiki:category-index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'wiki/category/delete.html'
    success_url = reverse_lazy('wiki:category-index')


class RequestListView(ListView):
    model = Request
    template_name = 'wiki/request/index.html'
    context_object_name = 'request'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        scan_for_requests()
        send_request_emails()
        return super().get(request, *args, **kwargs)


@csrf_exempt
def pa_create(request):
    # send_mail('Test email', 'Test message body.', 'testsender@sausagemachine.net', ['charles@sausagemachine.org'], fail_silently=False)

    # return redirect('wiki:page-index')

    ##############

    now = datetime.now()

    static_path = Path(settings.STATIC_ROOT)
    static_path.mkdir(exist_ok=True)

    create_log = settings.STATIC_ROOT / 'create_log.txt'
    with open(create_log, 'a+') as fh:
        fh.write(f'{now}: Received request\n')
        fh.write(f'headers: {request.headers}\n')
        fh.write(f'GET: {request.GET}\n')
        fh.write(f'POST: {request.POST}\n\n')
        response = request.POST.get('text')
        fh.write(f'POSTTEXT: {response}\n\n')

    # return HttpResponse(f'<p>Received at {now}.</p>')

    ##############

    response = request.POST.get('text', None)

    if response is not None:
        page_title_match = pattern_page_title.search(response)
        if page_title_match is not None:
            page_title = page_title_match.group(1)
            page_content = response[:response.find('~~~~')].strip()
            # page_content = page_content.replace('\r\n', '<br />')

            request = get_object_or_404(Request, page_title=page_title)

            page = Page(title=page_title, content=page_content)
            page.save()

            push_to_wiki(page)

            request.state = Request.RequestState.PAGE_UPDATED
            request.save()

    return redirect('wiki:pa-request-index')
