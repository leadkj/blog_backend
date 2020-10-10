from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import assets
import jenkinsapp.routing
import assets.routing

routinglist= []
routinglist.extend(jenkinsapp.routing.websocket_urlpatterns)
routinglist.extend(assets.routing.websocket_urlpatterns)

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routinglist
        )
    ),
})
