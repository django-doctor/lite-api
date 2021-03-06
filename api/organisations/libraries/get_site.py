from api.applications.models import BaseApplication, SiteOnApplication
from api.core.exceptions import NotFoundError
from api.organisations.models import Site


def get_site(pk, organisation) -> Site:
    try:
        return Site.objects.get(pk=pk, organisation=organisation)
    except Site.DoesNotExist:
        raise NotFoundError({"site": "Site not found - " + str(pk)})


def has_previous_sites(application: BaseApplication):
    return SiteOnApplication.objects.filter(application=application).exists()
