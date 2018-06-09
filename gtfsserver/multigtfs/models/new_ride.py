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
    new_route = models.BooleanField(default=False)
    route_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='The name of the route')
    route_description = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='A description of the route')
    notes = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Notes on the ride')
    vehicle_capacity = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='NUmber of passenger seats')
    vehicle_type = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What vehicle was used')
    vehicle_full = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Whether the vehicle was full')
    start_time = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What time the recording started')
    surveyor_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Who captured the ride')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.route.short_name, self.surveyor_name)
