from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path, path
from django.urls import include

from channels.auth import AuthMiddlewareStack
from product import consumers
# from product.routing import wsurlpatterns as websocket_urlpatterns

# urlpatterns = [
#     path('ws/product/', include('product.routing')),
# ]


websocket_urlpatterns = [
    path('ws/product/<str:product_name>/', consumers.ProductConsumer),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})