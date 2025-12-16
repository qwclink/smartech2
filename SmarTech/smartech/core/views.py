from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Category, Article, Banner, Guestbook
from .forms import RegisterForm, GuestbookForm
from .models import Order, OrderItem, Product
from .forms import OrderForm
from .cart import Cart
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin_orders.html', {'orders': orders})


@staff_member_required
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return redirect('admin_orders')

@login_required
def create_order(request):
    cart = Cart(request)
    cart_items = []

    for pid, quantity in cart.items():
        product = Product.objects.filter(id=pid).first()
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })

    total_sum = sum(item['total_price'] for item in cart_items)

    form = OrderForm(request.POST or None)

    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.save()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                quantity=item['quantity']
            )

        cart.cart.clear()
        request.session.modified = True

        return redirect('profile')

    return render(request, 'order_create.html', {
        'form': form,
        'cart_items': cart_items,
        'total_sum': total_sum
    })


def home(request):
    banners = Banner.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {'banners' : banners, 'products': products[:3]})

def product_list(request):
    products = Product.objects.all()
    q = request.GET.get('q')
    if q: products = products.filter(name__icontains=q)
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, pk):
    cart = Cart(request)
    cart.add(Product.objects.get(pk=pk))
    return redirect('cart')

def cart_view(request):
    cart = Cart(request)
    cart_items = []
    remove_ids = []

    for pid, quantity in cart.items():
        product = Product.objects.filter(pk=pid).first()
        if not product:
            remove_ids.append(pid)
            continue

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    for pid in remove_ids:
        del cart.cart[pid]

    request.session.modified = True

    total_sum = sum(item['total_price'] for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_sum': total_sum
    })



def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('profile')
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

def guestbook(request):
    form = GuestbookForm(request.POST or None)
    if form.is_valid(): form.save()
    messages = Guestbook.objects.all().order_by('-created_at')
    return render(request, 'guestbook.html', {'form': form, 'messages': messages})


from django.shortcuts import get_object_or_404
from .forms import ProductForm
from django.contrib import messages


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    products = Product.objects.all()
    messages_list = Guestbook.objects.all().order_by('-id')
    orders = Order.objects.all()

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Товар добавлен")
            return redirect('admin_panel')
    else:
        product_form = ProductForm()

    return render(request, 'admin_panel.html', {
        'products': products,
        'messages': messages_list,
        'product_form': product_form,
        'orders': orders
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Товар обновлён")
            return redirect('admin_panel')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Товар удалён")
    return redirect('admin_panel')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_message(request, pk):
    message = get_object_or_404(Guestbook, pk=pk)
    message.delete()
    messages.success(request, "Отзыв удалён")
    return redirect('admin_panel')

def logout(request):
    logout(request)

@staff_member_required
def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = 'completed'
    order.save()
    return redirect('admin_panel')

@staff_member_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = 'canceled'
    order.save()
    return redirect('admin_panel')