from django.urls import path
from games.views import AppRenderView, ShopView, ProductView, SearchView, HomeView

urlpatterns = [
    path('contact/', AppRenderView.as_view(), name="contact"),
    path('shop/', ShopView.as_view(), name="shop"),
    path('search/', SearchView.as_view(), name='search'),
    path('', HomeView.as_view(), name="home"),
    path('shop/<int:game_id>/', ProductView.as_view(), name="product-details"),
]
