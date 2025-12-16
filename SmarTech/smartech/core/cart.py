class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})
        self.session['cart'] = self.cart

    def add(self, product):
        pid = str(product.id)
        self.cart[pid] = self.cart.get(pid, 0) + 1
        self.session.modified = True

    def items(self):
        return self.cart.items()
