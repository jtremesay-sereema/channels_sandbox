import os

from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path, re_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")

from app import consumers

application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                path("foo", consumers.EntryPointAsyncHttpConsumer.as_asgi()),
                re_path(r"", get_asgi_application()),
            ]
        ),
        "channel": ChannelNameRouter({"foo": consumers.WorkerSyncConsumer.as_asgi()}),
    }
)
