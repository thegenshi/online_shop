from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from apps.main.models import Product, Category, Customer, Order
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.contrib import messages
from django.views.generic.base import TemplateView
from common.view import TitleMixin

# Create your views here.

# def main(request):
#     product = Product.objects.all()
#     category = Category.objects.all()
#     return render(request, 'index.html', {'product':product, 'category':category})
class BaseView(TitleMixin, TemplateView):
    template_name = 'test.html'
    title = 'Gadgets'


class MainListView(TitleMixin, ListView):
    model = Product
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        cache_category = cache.get('category')
        if not cache_category:
            category = Category.objects.all()
            cache.set('category', category, 10)
        else:
            category = cache_category
        category = Category.objects.all()
        product = Product.objects.all()
        context['category'] = category
        context['product'] = product
        return context


# def info(request, id):
#     info = Product.objects.get(id = id)
#     return render(request, 'info.html', {'info':info})

class InfoView(TemplateView):
    template_name = 'info.html'
    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        info = Product.objects.get(id = self.kwargs['id'])
        context['info'] = info
        return context


@login_required(login_url="login")
def add_to_cart(request, id):
    cart_session = request.session.get('cart_session1', [])
    cart_session.append(id)
    request.session['cart_session1'] = cart_session
    print(cart_session)
    return HttpResponseRedirect('/')

# class Add_to_cartView(TemplateView):
#     template_name = 'index.html'
#     def get_context_data(self, **kwargs):
#         context = super(Add_to_cartView, self).get_context_data(**kwargs)
#         cart_session = self.request.session.get('cart_session1', [])
#         cart_session.append(self.kwargs['id'])
#         self.request.session['cart_session1'] = cart_session
#         print(cart_session)
#         context['cart_session'] = cart_session
#         return context

    # def dispatch(self, request, *args, **kwargs):
    #     return redirect('main')


# @login_required(login_url="login")
# def cart(request):
#     cart_session = request.session.get('cart_session1', [])
#     amount = len(cart_session)
#     products = Product.objects.filter(id__in = cart_session)
#     total_price = 0
#     for i in products:
#         i.count = cart_session.count(i.id)
#         i.sum = i.count * i.price
#         total_price += i.sum
#     context = {'products':products, 'amount':amount, 'total_price':total_price}
#     return render(request, 'cart.html', context)

class CartView(TemplateView, TitleMixin):
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        # cache_product = cache.get('product')
        # if not cache_product:
        #     product = Product.objects.filter(id__in = cart_session)
        #     cache.set('product', product, 10)
        # else:
        #     product = cache_product
        cart_session = self.request.session.get('cart_session1', [])
        amount = len(cart_session)
        count_of_product = len(cart_session)
        products = Product.objects.filter(id__in = cart_session)
        total_price = 0
        for i in products:
            i.count = cart_session.count(i.id)
            i.sum = i.count * i.price
            total_price += i.sum
        context['products'] = products
        context['amount'] = amount
        context['total_price'] = total_price
        context['count_of_product'] = count_of_product
        return context


def remove(request, id):
    cart_session = request.session.get('cart_session1', [])
    g = cart_session
    g.remove(id)
    print(g)
    request.session['cart_session'] = g
    return HttpResponseRedirect('/')

def search(request):
    if request.method == "POST":
        product = request.POST.get('product')
        product_model = Product.objects.filter(title__contains = product)
        return render(request , 'search.html', {'product':product_model})

# class SearchView(TemplateView):
#     template_name = 'search.html'
#     def get_context_data(self, **kwargs):
#         context = super(SearchView, self).get_context_data(**kwargs)
#         if self.request.method == "POST":
#             product = self.request.POST.get('product')
#             product_model = Product.objects.filter(title__contains = product)
#             context['product'] = product
#             context['product_model'] = product_model
#             return context


# def category(request, slug):
#     category = Category.objects.get(slug = slug)
#     product = Product.objects.filter(category = category)
#     return render(request,'category.html',{'product':product, 'category':category})

class CategoryView(ListView):
    model = Category
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        cat = Category.objects.all()
        category = Category.objects.get(slug = self.kwargs['slug'])
        product = Product.objects.filter(category = category)
        context['cat'] = cat
        context['products'] = product
        return context

# def contact_us(request):
#     return render(request, 'contact_us.html')

class AboutusView(TemplateView):
    template_name = 'contact_us.html'


def order(request):
    if request.method == 'POST':
        cart_session = request.session.get('cart_session', [])
        if len(cart_session) == 0:
            messages.error(request, 'Ваша корзина пустая', extra_tags='danger')
            return redirect('cart')
        else:
            customer = Customer()
            customer.name = request.POST.get('c_name')
            customer.last_name = request.POST.get('c_lastname')
            customer.number = request.POST.get('c_number')
            customer.addres = request.POST.get('c_addres')
            customer.message = request.POST.get('c_message')
            customer.save()
            for i in range(len(cart_session)):
                order = Order()
                order.product = Product.objects.get(id=cart_session[i])
                order.customer = customer
                order.price = order.product.price
                order.phone = customer.number
                order.addres = customer.addres
                order.save()

            request.session['cart_session'] = []
            messages.error(request, 'Заказ успешно отправлено!', extra_tags='success')
            return redirect('cart')