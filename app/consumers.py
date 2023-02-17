import asyncio
import datetime

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.generic.http import AsyncHttpConsumer


class EntryPointAsyncHttpConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        # Send headers
        await self.send_headers(
            headers=[
                (b"Content-Type", b"text/plain"),
            ]
        )

        # Create the task
        await self.channel_layer.send(
            "foo",
            {
                "type": "foo.do_something",
                "channel_name": self.channel_name,
                "timestamp": datetime.datetime.now().timestamp(),
            },
        )

        # Headers are only sent after the first body event.
        await self.send_body(b"", more_body=True)

    async def foo_on_something_done(self, event):
        print("on_something_done", event)

        await self.send_body(event["timestamp"].encode())

        print("done")


class WorkerSyncConsumer(SyncConsumer):
    def foo_do_something(self, event):
        print("do_something", event)

        async_to_sync(self.channel_layer.send)(
            event["channel_name"],
            {"type": "foo.on_something_done", "timestamp": event["timestamp"]},
        )

        print("done")
