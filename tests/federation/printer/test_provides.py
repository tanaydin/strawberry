# type: ignore

import textwrap
from typing import List

import strawberry
from strawberry.schema.config import StrawberryConfig


def test_field_provides_are_printed_correctly_camel_case_on():
    global Review

    @strawberry.federation.type
    class User:
        username: str

    @strawberry.federation.type(keys=["upc"], extend=True)
    class Product:
        upc: str = strawberry.federation.field(external=True)
        the_name: str = strawberry.federation.field(external=True)
        reviews: List["Review"]

    @strawberry.federation.type
    class Review:
        body: str
        author: User
        product: Product = strawberry.federation.field(provides=["name"])

    @strawberry.federation.type
    class Query:
        @strawberry.field
        def top_products(self, first: int) -> List[Product]:
            return []

    schema = strawberry.federation.Schema(
        query=Query, config=StrawberryConfig(auto_camel_case=True)
    )

    expected = """
        directive @external on FIELD_DEFINITION

        directive @key(fields: _FieldSet!, resolvable: Boolean = true) on OBJECT | INTERFACE

        directive @provides(fields: _FieldSet!) on FIELD_DEFINITION

        extend type Product @key(fields: "upc") {
          upc: String! @external
          theName: String! @external
          reviews: [Review!]!
        }

        type Query {
          _service: _Service!
          _entities(representations: [_Any!]!): [_Entity]!
          topProducts(first: Int!): [Product!]!
        }

        type Review {
          body: String!
          author: User!
          product: Product! @provides(fields: "name")
        }

        type User {
          username: String!
        }

        scalar _Any

        union _Entity = Product

        scalar _FieldSet

        type _Service {
          sdl: String!
        }
    """

    assert schema.as_str() == textwrap.dedent(expected).strip()

    del Review


def test_field_provides_are_printed_correctly_camel_case_off():
    global Review

    @strawberry.federation.type
    class User:
        username: str

    @strawberry.federation.type(keys=["upc"], extend=True)
    class Product:
        upc: str = strawberry.federation.field(external=True)
        the_name: str = strawberry.federation.field(external=True)
        reviews: List["Review"]

    @strawberry.federation.type
    class Review:
        body: str
        author: User
        product: Product = strawberry.federation.field(provides=["name"])

    @strawberry.federation.type
    class Query:
        @strawberry.field
        def top_products(self, first: int) -> List[Product]:
            return []

    schema = strawberry.federation.Schema(
        query=Query, config=StrawberryConfig(auto_camel_case=False)
    )

    expected = """
        directive @external on FIELD_DEFINITION

        directive @key(fields: _FieldSet!, resolvable: Boolean = true) on OBJECT | INTERFACE

        directive @provides(fields: _FieldSet!) on FIELD_DEFINITION

        extend type Product @key(fields: "upc") {
          upc: String! @external
          the_name: String! @external
          reviews: [Review!]!
        }

        type Query {
          _service: _Service!
          _entities(representations: [_Any!]!): [_Entity]!
          top_products(first: Int!): [Product!]!
        }

        type Review {
          body: String!
          author: User!
          product: Product! @provides(fields: "name")
        }

        type User {
          username: String!
        }

        scalar _Any

        union _Entity = Product

        scalar _FieldSet

        type _Service {
          sdl: String!
        }
    """

    assert schema.as_str() == textwrap.dedent(expected).strip()

    del Review