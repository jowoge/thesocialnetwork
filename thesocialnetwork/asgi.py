"""
ASGI config for thesocialnetwork project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import the_app.routing  # Import your routing configuration here

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thesocialnetwork.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            the_app.routing.websocket_urlpatterns
        )
    ),
})
