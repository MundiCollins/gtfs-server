# model for new rides from twigatatu

from __future__ import unicode_literals
from logging import getLogger
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


logger = getLogger(__name__)


@python_2_unicode_compatible
class Ride(Base):
    """A ride along a given route

    To reference new stops data in the GTFS feed.
    """
    route = models.ForeignKey('Route')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.route.route_id
