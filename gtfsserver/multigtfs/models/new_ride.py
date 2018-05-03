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
    desc = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Description of the ride.')
    notes = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Notes on the ride.')
    vehicle_capacity = models.IntegerField(
        blank=True, null=True,
        help_text="Number of passenger seats in the vehicle")
    vehicle_type = models.CharField(
        max_length=1, blank=True, null=True,
        choices=(
            ('0', 'Matatu'),
            ('1', 'Bus'),
            ('2', 'TukTuk')),
        help_text='What type of vehicle are you in?')
    start_time = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What time did the ride start?'
    )
    route_latitude = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='WGS 84 latitude of stop or station')
    route_longitude = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='WGS 84 latitude of stop or station')
    extra_data = JSONField(default={}, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.route.route_id
