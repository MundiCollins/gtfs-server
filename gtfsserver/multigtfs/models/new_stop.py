# model for new stops from twigatatu

from __future__ import unicode_literals
from logging import getLogger
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


logger = getLogger(__name__)


@python_2_unicode_compatible
class NewStop(Base):
    """A stop captured during a ride

    To reference new stops data in the GTFS feed.
    """
    ride = models.ForeignKey('Ride')
    stop_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What is the name of the stop?'
    )
    stop_designation = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What is the official designation status of the stop?'
    )
    latitude = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='WGS 84 latitude of stop or station')
    longitude = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='WGS 84 latitude of stop or station')
    arrival_time = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What time did the ride arrive?'
    )
    departure_time = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='What time did the ride arrive?'
    )
    board = models.CharField(
        max_length=255, blank=True, null=True,
    )
    alight = models.CharField(
        max_length=255, blank=True, null=True,
    )
    extra_data = JSONField(default={}, blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.latitude, self.longitude)