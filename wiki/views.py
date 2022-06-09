from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import FormView

from .models import Page
from .forms import PageForm
from .mediawiki import push_to_wiki


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

    if request.method == 'POST':
        active_links = [int(pk) for pk in request.POST.getlist('link[]')]

        for link in links:
            link.active = (link.pk in active_links)
            link.save()

        push_to_wiki(page)

    context = {'page': page, 'links': links}

    return render(request, 'wiki/page/push.html', context)