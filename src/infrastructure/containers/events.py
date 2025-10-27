from dependency_injector import containers, providers

from src.applications.event_members.containers import EventMemberApplications
from src.applications.events.containers import EventApplications
from src.infrastructure.events.containers import Gateways, Repositories

class App(containers.DeclarativeContainer):
    gateways = providers.Container(Gateways)

    repositories = providers.Container(Repositories)

    event_applications = providers.Container(EventApplications)

    event_member_applications = providers.Container(EventMemberApplications)
