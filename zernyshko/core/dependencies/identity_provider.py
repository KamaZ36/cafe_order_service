from dishka import Provider, Scope, from_context, provide
from fastapi import Request

from zernyshko.infrastructure.identity_provider.base import (
    IdentityProvider,
    SessionIdGetter,
)
from zernyshko.infrastructure.identity_provider.http import (
    CookieSessionIdGetter,
    HTTPIdentityProvider,
)
from zernyshko.infrastructure.repositories.session.base import BaseSessionRepository
from zernyshko.infrastructure.repositories.user.base import BaseUserRepository


class IdentityProviderProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide
    def session_id_getter(self, request: Request) -> SessionIdGetter:
        return CookieSessionIdGetter(request)

    @provide
    def http_identity_provider(
        self,
        session_id_getter: SessionIdGetter,
        session_repository: BaseSessionRepository,
        user_repository: BaseUserRepository,
    ) -> IdentityProvider:
        return HTTPIdentityProvider(
            session_id_getter=session_id_getter,
            session_repository=session_repository,
            user_repository=user_repository,
        )
