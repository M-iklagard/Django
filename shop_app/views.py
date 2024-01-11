from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views import View
from rest_framework.response import Response
from shop_app.models import Product
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .serializers import WarehouseSerializer
from .forms import get_wh, get_cities
from django.http import JsonResponse
import math
from django.views.decorators.csrf import csrf_exempt

class RegView(View):
    """Відображення форми реєстрації"""

    def get(self, request):
        """Рендерить форму"""
        form = RegForm()
        return render(request, context={"form":form}, template_name="reg.html")

    def post(self, request):
        """Реєструє користувача"""
        form = RegForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # створюємо користувача
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # створюємо кошик
            cart = Cart.objects.create(customer=user)
            cart.save()

            return redirect("auth")
        else:
            return HttpResponse("Помилка")

class AuthView(View):
    """Форма авторизації"""

    def get(self, request):
        """Рендерить форму"""
        form = AuthForm()
        return render(request, context={"form": form}, template_name="auth.html")

    def post(self, request):
        """Авторизує користувача"""
        form = AuthForm(request.POST)

        username = form.data["username"]
        password = form.data["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user=user)
            return redirect("/main/all/1")
        else:
            print(form.errors)
            return HttpResponse("Щось не так")

class Main(View):
    """Виводить продукти - типу головна сторінка"""
    def pagination(self, page, category):
        """Фігня для пагінації, повертає три значення,
        початок зрізу, кінець зрізу та кількість сторінок продуктів"""

        if category=="all":
            page_count = math.ceil(Product.objects.all().count()/15)+1
        else:
            category_obj = Category.objects.get(name=category)
            page_count = math.ceil(Product.objects.all().filter(category=category_obj).count() / 15) + 1
            print(category_obj)
        if page == 0:
            start = 0
            stop = 15

        else:
            stop = (16*page)-1
            start = stop-16
            if start<0:
                start=0

        return start, stop, page_count


    def get(self, request, category, page):
        start, stop, pages_count = self.pagination(page, category)
        if category == "all":
            products = Product.objects.all()
        else:
            # перевіряємо чи існує категорія
            try:
                category_obj = Category.objects.get(name=category)
            except: return HttpResponse("Категорія не існує")
            # продукти за категорією
            products = Product.objects.all().filter(category=category_obj)

        # ---------критерії фільтрування ----------
        filter = FilterForm(request.GET)
        f_criterials = filter.data.dict()

        try:
            ram = int(f_criterials["ram"])
        except: ram=None
        try:
            rom = int(f_criterials["rom"])
        except: rom=None
        try:
            display = int(f_criterials["display"])
        except: display=None
        try:
            brand = f_criterials["brand"]
        except:
            brand = None
        if brand:
            pass
        else:
            brand=None

        filters = [ram, rom, display, brand]
        # ---------критерії фільтрування ----------/


        # ----------логіка фільтрування--------------
        if ram or rom or display or brand:
            if ram:
                products = products.filter(ram__gt=ram)
            if rom:
                products = products.filter(rom__gt=rom)
            if display:
                products = products.filter(display__gt=display)
            if brand:
                products = products.filter(brand__contains=brand)
            products[start:stop]

            # змінюємо кількість сторінок, якщо товарів менше 15
            if len(products)<=15:
                pages_count = 2
        else:
            products = products[start:stop]
        # ----------логіка фільтрування--------------/

        # всі категорії для дроп меню
        categories = Category.objects.all()
        responce = render(request, 'main.html', {'products': products,
                                                 "pages_count": range(1, pages_count),
                                                 "current_page": page,
                                                 "current_category": category,
                                                 "categories": categories,
                                                 "filter": filter})


        # перевіряємо чи користувач не авторизований
        if not request.user.is_authenticated:
            # перевіряємо чи він вже має неавторизовану корзину
            try:
                cart_id = request.COOKIES["cart_id"]
            except:
                # якщо не має, то створюємо неавторизовану корзину
                unautorized_cart = Cart.objects.create(customer=None)
                responce.set_cookie("cart_id", unautorized_cart.id)
        return responce

class CartView(View):
    """Відповідає за логіку корзини"""
    def get(self, request):

        # якщо користувач авторизований
        if request.user.is_authenticated:
            cart = Cart.objects.get(customer=request.user)
            data = cart.items()
            cart_id = cart.id
            return render(request, context={"cart": data, "order_form": OrderForm, "bio_form": BioForm, "cart_id": cart_id}, template_name='cart.html')

        # якщо користувач не авторизований
        else:
            # перевіряємо чи існує cart_id
            try:
                cart_id = request.COOKIES["cart_id"]
            except:
                # якщо у користувача немає неавторизованої корзини
                unautorized_cart = Cart.objects.create(customer=None)
                products = unautorized_cart.products.all()
                responce = render(request, 'cart.html', {'cart': products})
                responce.set_cookie("cart_id", unautorized_cart.id)
                return responce

            # якщо у крористувача є неавторизована корзина
            cart = Cart.objects.get(id=cart_id)
            data = cart.items()
            cart_id = cart.id
            return render(request, context={"cart": data, "order_form": OrderForm, "bio_form": BioForm, "cart_id": cart_id}, template_name='cart.html')

class AddToCartBtn(View):
    def post(self, request):
        new_product_id = request.POST["product_id"]
        redirect_to = request.POST["redirect_to"]
        print(redirect_to)
        # додвання товару в авторизовану корзину
        if request.user.is_authenticated:

            # отримуємо корзину користувача, та новий продукт
            cart = Cart.objects.get(customer=request.user)
            new_product = Product.objects.get(id=new_product_id)

            # отриуємо айтеми корзини
            his_items = CartItem.objects.filter(cart_id=cart.id)

            # якщо в айтемі вже є такий продукт то змінюємо кількість
            for item in his_items:
                if item.product_id == int(new_product_id):
                    item.amount += 1
                    item.save()

            # print(his_items.values())
            cart.products.add(new_product)

        # якщо користувач не авторизований
        else:
            try:
                # отримуємо айді неавторизованої корзини
                cart_id = request.COOKIES["cart_id"]
            except:
                return HttpResponse("неавторизована корзина не існує") # тут можна прописати логіку створення корзини
            cart = Cart.objects.get(id=cart_id)
            new_product = Product.objects.get(id=new_product_id)

            # отриуємо айтеми корзини
            his_items = CartItem.objects.filter(cart_id=cart.id)

            # якщо в айтемі вже є такий продукт то змінюємо кількість
            for item in his_items:
                if item.product_id == int(new_product_id):
                    item.amount += 1
                    item.save()

            # print(f"це неавторизована корзина {his_items.values()}")
            cart.products.add(new_product)

        return redirect(f"{redirect_to}")

class LogOut(View):

    def get(self, request):
        logout(request)
        return redirect("/main/all/1")

@api_view(['GET'])
def api(request, city_ref):
    """Апі яке повертатитме відділення нової пошти
    за певним ref міста"""
    war = get_wh(city_ref)
    data = {"warehouse": war}
    serializer_obj = WarehouseSerializer(data)
    return Response(serializer_obj.data)

class ProductView(View):

    def get(self, request, product_id):

        product = Product.objects.get(id=product_id)
        # всі категорії для дроп меню
        categories = Category.objects.all()
        return render(request,context={"product": product, "categories":categories, "is_main":1}, template_name="product.html")

class SearchView(View):
    """Вью для форми пошуку,
    до нього робить запит javaScript"""
    def get(self, request, criterial):

        products = Product.objects.all().filter(name__contains=criterial)
        data = []
        for product in products:
            data.append([product.id, product.name])

        return JsonResponse(data, safe=False)

class RedirectMain(View):
    """Це клас для редіректу з базової адреси до першї сторінки
    каталогу товарів"""
    def get(self, request):
        return redirect("main", category="all", page=1)

def send_order(message):
    """Ця фігня відправить повідомлення манагеру"""
    TOKEN = "6361419585:AAFSJwZxG7WOp96PazxiibAt48J5STMmy3A"
    chat_id = 398324319
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    params = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, params=params)

def order(request):
    data = ["Помилка в view order"]

    if request.method == "POST":

        # очищуємо корзину
        order_data =  json.loads(request.body.decode())
        cart_to_clear = Cart.objects.get(id=order_data["cart_id"])
        # видаляємо айтеми корзини
        cart_items = CartItem.objects.all().filter(cart=cart_to_clear).delete()

        # функція історії замовлень доступна лише авторизованим користувачам
        if cart_to_clear.customer:

            #  це дані про товари замовлення
            products_names = order_data["prodNamesArray"]
            products_prices = order_data["prodPricesArray"]
            products_amounts = order_data["prodAmountsArray"]

            prod_data = []
            for i in range(len(products_names)):
                prod_data.append([products_names[i], products_prices[i], products_amounts[i]])
            # -----------------------------------------------------------------

            # записуємо дані замовлення в бд
            order = Order.objects.create(
                cart=cart_to_clear,
                name=order_data["name"],
                surname=order_data["surname"],
                patronymic=order_data["patronymic"],
                phone=order_data["phone"],
                selectedcity=order_data["selectedcity"],
                selectedwarehouse=order_data["selectedWarehouse"],
                products=prod_data,
                status="Виконується")

            send_order(str(prod_data))
            print(str(prod_data))
            data = ["Успішно view order"]

            # треба надіслати замовлення в телегу

        return JsonResponse(data, safe=False)

class OrderStory(View):
    """Історія замовлень для авторизованих користувачів"""
    def get(self, request):
        if request.user.is_authenticated:
            cart_id = Cart.objects.get(customer=request.user).id
            orders = Order.objects.all().filter(cart_id=cart_id)

            categories = Category.objects.all()
            return render(request, template_name="order_story.html", context={"categories": categories, "orders": orders, "is_main":1})

class CartDelButton(View):
    def post(self, request):
        cart_item_id = request.POST["cart_item_id"]
        CartItem.objects.get(id=cart_item_id).delete()
        return redirect("cart")