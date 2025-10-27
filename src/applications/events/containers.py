from dependency_injector import containers, providers

from src.applications.events.delete import EventDelete
from src.applications.events.get_list import GetEventList
from src.applications.events.create import CreateEvent
from src.applications.events.remind import EventRemind
from src.applications.events.update import EventUpdate
from src.infrastructure.events.containers import Repositories


class EventApplications(containers.DeclarativeContainer):
    get_event_list = providers.Singleton(
        GetEventList,
        repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )

    create_event = providers.Singleton(
        CreateEvent,
        event_repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )

    delete_event = providers.Singleton(
        EventDelete,
        repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )

    remind_event = providers.Singleton(
        EventRemind,
        event_repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )

    update_event = providers.Singleton(
        EventUpdate,
        repository=Repositories.event_repository,
        event_member_repository=Repositories.event_member_repository,
    )