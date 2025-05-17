import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # Import your chat routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Set your settings module

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Django's regular HTTP handling
    "websocket": AuthMiddlewareStack(  # WebSocket handler with authentication
        URLRouter(
            chat.routing.websocket_urlpatterns  # Your WebSocket routes from chat/routing.py
        )
    ),
})
