from dependency_injector import containers, providers

import src.infrastructure.events.db as db

from src.infrastructure.events.repositories import EventRepository, EventMemberRepository

class Gateways(containers.DeclarativeContainer):
    db_credential_provider = providers.Singleton(
        db.DBCredentialProvider,
    )

    db_connect_factory = providers.Singleton(
        db.DBConnectFactory,
        cred_provider=db_credential_provider,
    )

class Repositories(containers.DeclarativeContainer):
    event_repository = providers.Singleton(
        EventRepository,
        db_connect_factory=Gateways.db_connect_factory,
    )

    event_member_repository = providers.Singleton(
        EventMemberRepository,
        db_connect_factory=Gateways.db_connect_factory,
    )
