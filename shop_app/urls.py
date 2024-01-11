from django.urls import path
from .views import *


urlpatterns = [
    path("reg/", RegView.as_view(), name="reg"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("main/<str:category>/<int:page>/", Main.as_view(), name="main"),
    path("cart/", CartView.as_view(), name="cart"),
    path("add_to_cart/", AddToCartBtn.as_view(), name="add_to_cart"),
    path("logout/", LogOut.as_view(), name="logout"),
    path("api/<str:city_ref>/", api, name="api"),
    path("product/<int:product_id>/", ProductView.as_view(), name="product_page"),
    path("search/<str:criterial>/", SearchView.as_view(), name="search"),
    path("", RedirectMain.as_view(), name="main-redir" ),
    path("order/", order, name="order"),
    path("orderstory/", OrderStory.as_view(), name="order_story"),
    path("cartdelbutton", CartDelButton.as_view(), name="cartdelbutton")
]
