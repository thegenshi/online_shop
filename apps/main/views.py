from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from apps.main.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from django.views.generic.base import TemplateView
# Create your views here.

# def main(request):
#     product = Product.objects.all()
#     category = Category.objects.all()
#     return render(request, 'index.html', {'product':product, 'category':category})

class MainListView(ListView):
    model = Product
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
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

class CartView(TemplateView):
    template_name = 'cart.html'
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart_session = self.request.session.get('cart_session1', [])
        amount = len(cart_session)
        products = Product.objects.filter(id__in = cart_session)
        total_price = 0
        for i in products:
            i.count = cart_session.count(i.id)
            i.sum = i.count * i.price
            total_price += i.sum
        context['products'] = products
        context['amount'] = amount
        context['total_price'] = total_price
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
