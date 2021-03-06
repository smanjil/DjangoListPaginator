# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import (
    render,
    HttpResponseRedirect, 
    reverse
)
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from genericviews.forms import ProductForm
from genericviews.models import Product

import logging

genericviews_logger = logging.getLogger(__name__)

# Create your views here.

class CreateProductView(LoginRequiredMixin, generic.FormView):
    model = Product
    form_class = ProductForm
    template_name = 'genericviews/makeentry.html'

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        genericviews_logger.info('Product create form requested!! by user {0}...' .format(request.user))
        return render(request, 'genericviews/makeentry.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        title = form.data['title']
        desc = form.data['desc']

        Product.objects.create(
            user = request.user, 
            title = title, 
            desc = desc
        )

        form = ProductForm()

        messages.add_message(
            request, 
            messages.SUCCESS, 
            'You have successfully created a product!'
        )
        genericviews_logger.info('New product created by user {0}...' .format(request.user))
        return HttpResponseRedirect('/genericviews/')

class IndexView(LoginRequiredMixin, generic.ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'genericviews/index.html'
    paginate_by = 2

    login_url = '/users/login'
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        empty_values_list = list(filter(lambda x: x == '', self.request.GET.values()))
        total_len = len(self.request.GET.keys()) - 1
        if len(empty_values_list) < total_len:
            # get datas from filter form
            genericviews_logger.info('Getting filter data for user {0}...' .format(self.request.user))

            record_id = self.request.GET.get('record-id', None)
            product_title = self.request.GET.get('product-title', None)

            if record_id and product_title:
                genericviews_logger.info('Product listing according to record id and product title for user {0}...' .format(self.request.user))
                return Product.objects.all().filter(user = self.request.user).filter(id = record_id).filter(title = product_title).order_by('id')
            elif record_id:
                genericviews_logger.info('Product listing according to record id for user {0}...' .format(self.request.user))
                return Product.objects.all().filter(user = self.request.user).filter(id = record_id).order_by('id')
            elif product_title:
                genericviews_logger.info('Product listing according to product title for user {0}...' .format(self.request.user))   
                return Product.objects.all().filter(user = self.request.user).filter(title = product_title).order_by('id')
        else:
            genericviews_logger.info('Product listing for user {0}...' .format(self.request.user))
            return Product.objects.all().filter(user = self.request.user).order_by('id')

    def get_paginate_by(self, queryset):
        if 'paginate_by' in self.request.GET:
            self.request.session['paginate_by'] = self.request.GET['paginate_by']
            self.paginate_by = self.request.session.get('paginate_by', self.paginate_by)
        elif 'page' in self.request.GET:
            self.paginate_by = self.request.session.get('paginate_by', self.paginate_by)
        else:
            if 'paginate_by' in self.request.session:
                del self.request.session['paginate_by']

        return self.paginate_by

class DetailsView(LoginRequiredMixin, generic.DetailView):
    model = Product
    template_name = 'genericviews/detail.html'

    login_url = '/users/login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)

        genericviews_logger.info('Product detail for product id {0} by user {1}...' .format(self.kwargs['pk'], self.request.user))

        context['new_list'] = Product.objects.all().filter(~Q(user = self.request.user)).order_by('id')

        return context

class EditView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    fields = ['title', 'desc']
    template_name_suffix = '_update_form'

    login_url = '/users/login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        messages.add_message(
            self.request, 
            messages.SUCCESS, 
            'You have successfully update the product!'
        )
        genericviews_logger.info('Product update successful for product id {0} by user {1}...' .format(self.kwargs['pk'], self.request.user))
        return reverse('genericviews:detail', kwargs = {'pk': self.kwargs['pk']})

class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product

    login_url = '/users/login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self):
        pid = self.kwargs['pk']
        messages.add_message(
            self.request, 
            messages.SUCCESS, 
            'You have successfully deleted a product!'
        )
        genericviews_logger.info('Product {0} deleted by user {1}...' .format(pid, self.request.user))
        return reverse('genericviews:index')

class MultipleDeleteView(LoginRequiredMixin, generic.FormView):
    model = Product

    login_url = '/users/login'
    redirect_field_name = 'redirect_to'

    def post(self, request, *args, **kwargs):
        # get list of checkbox values
        product_ids = list(map(lambda id: int(id), request.POST.getlist('ids')))

        # delete rows from Product model having those ids
        prod_obj = Product.objects.filter(pk__in = product_ids).delete()
        
        # redirect to index page
        messages.add_message(
            request, 
            messages.SUCCESS, 
            'You have successfully deleted {0} product!' .format(len(product_ids))
        )
        genericviews_logger.info('Products deleted by user {0}...' .format(request.user))
        return HttpResponseRedirect('/genericviews/')

class FilterView(LoginRequiredMixin, generic.FormView):
    pass