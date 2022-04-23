from __future__ import annotations

from random import randint
from typing import Dict, Optional

from typing_extensions import Literal

from sanic import Sanic
from strawberry.sanic.views import GraphQLView as BaseGraphQLView

from ..schema import Query, schema
from . import JSON, HttpClient, Response


class GraphQLView(BaseGraphQLView):
    def get_root_value(self):
        return Query()


class SanicHttpClient(HttpClient):
    def __init__(self, graphiql: bool = True):
        self.app = Sanic(
            f"test_{int(randint(0, 1000))}",
            log_config={
                "version": 1,
                "loggers": {},
                "handlers": {},
            },
        )
        self.app.add_route(
            GraphQLView.as_view(schema=schema, graphiql=graphiql), "/graphql"
        )

    async def _request(
        self, method: Literal["get", "post"], url: str, **kwargs
    ) -> Response:
        request, response = await self.app.asgi_client.request(method, url, **kwargs)

        return Response(status_code=response.status_code, data=response.content)

    async def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> Response:
        return await self._request("get", url, headers=headers)

    async def post(
        self, url: str, json: JSON, headers: Optional[Dict[str, str]] = None
    ) -> Response:
        return await self._request("post", url, json=json, headers=headers)