from dependency_injector import containers, providers

from src.applications.event_members.invite import EventMemberInvite
from src.applications.event_members.leave import EventMemberLeave
from src.infrastructure.events.containers import Repositories


class EventMemberApplications(containers.DeclarativeContainer):
    invite = providers.Singleton(
        EventMemberInvite,
        event_repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )

    leave = providers.Singleton(
        EventMemberLeave,
        event_repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )
