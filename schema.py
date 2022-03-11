from datetime import datetime
from typing import List

import strawberry
from strawberry import ID
from strawberry.schema.types.base_scalars import DateTime


async def full_info_2(root) -> str:
    return f'{root.name}, {root.age}, {root.date_created}'


# Types
@strawberry.type
class User:
    _id: ID
    name: str
    age: int
    email: str
    password: str
    date_created: DateTime

    @strawberry.field
    def full_info(self) -> str:
        return f'{self.name}, {self.age}, {self.date_created}'

    # Field as root python function
    full_info_2: str = strawberry.field(resolver=full_info_2)


@strawberry.type
class Event:
    _id: ID
    title: str
    description: str
    price: float
    date: DateTime
    creator: User


@strawberry.type
class AuthData:
    user_id: ID
    token: str
    token_expiration: int


@strawberry.type
class Booking:
    _id: ID
    event: Event
    user: User
    created_at: DateTime
    updated_at: DateTime


############## Input Types ##################
@strawberry.input
class EventInput:
    title: str
    description: str
    price: float
    date: DateTime


@strawberry.input
class UserInput:
    email: str
    password: str


# Query Resolver
async def get_all_users(id: strawberry.ID) -> List[User]:
    return [User(name="Patrick", age=100, date_created=datetime.now()),
            User(name="Patrick 2", age=100, date_created=datetime.now())]


async def get_all_event() -> List[Event]:
    pass


async def get_all_bookings() -> List[Booking]:
    pass


async def login(email: str, name: str, password: str):
    pass


@strawberry.type
class RootQuery:
    # First way to attach a RESOLVER
    users: List[User] = strawberry.field(resolver=get_all_users)

    events: List[Event] = strawberry.field(resolver=get_all_event)
    bookings: List[Booking] = strawberry.field(resolver=get_all_bookings)
    login: AuthData = strawberry.field(resolver=login)

    # Second way to attach a RESOLVER
    # Co-locate resolvers and types or when you have very small resolvers
    @strawberry.field
    def user(self, id: int, email: str) -> User:
        return User(name="Patrick", age=100, date_created=datetime.now())

    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class RootMutation:
    @strawberry.mutation
    def create_user(self, name: str, age: int) -> User:
        # info.context["background_tasks"].add_task(notify_new_flavour, name)
        user = User(name, age, datetime.now())
        return user


schema = strawberry.Schema(query=RootQuery, mutation=RootMutation)
