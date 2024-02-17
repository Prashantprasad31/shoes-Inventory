from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('register/', views.register_user),
    # path('login/', views.login_user),
    path('home/', views.home),
    # path('logout/', views.u_logout),
    path('product/', views.product),
    path('filter/<category_value>', views.filter_by_category),
    path('sort/<sort_value>', views.sort_by_price),
    path('rate/<rate_value>', views.sort_by_rating),
    path('pricer', views.sort_by_price_range),
    path('product_detail/<pid>', views.product_detail),
    path('add_to_cart/<pid>', views.add_to_cart),
    path('cartview/', views.cart_data),
    path('remove/<cartid>', views.remove_item),
    path('search', views.search_by_sku),
]
urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)