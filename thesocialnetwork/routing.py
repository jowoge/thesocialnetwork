# used to reach different channel requests to different parts of the  app
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import the_app.routing

# declare new version of our application
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            the_app.routing.websocket_urlpatterns
            )
    ),
})