# model for new fares from twigatatu

from __future__ import unicode_literals
from logging import getLogger
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

from multigtfs.models.base import models, Base


logger = getLogger(__name__)


@python_2_unicode_compatible
class NewFare(Base):
    """A new fare entry

    """
    stop_to = models.CharField(
        max_length=255, blank=True, null=True,)
    stop_from = models.CharField(
        max_length=255, blank=True, null=True,)
    amount = models.CharField(
        max_length=255, blank=True, null=True,)
    stop_from_id = models.CharField(
        max_length=255, blank=True, null=True,)
    route_id = models.CharField(
        max_length=255, blank=True, null=True,)
    stop_to_id = models.CharField(
        max_length=255, blank=True, null=True,)
    weather = models.CharField(
        max_length=255, blank=True, null=True,)
    traffic_jam = models.CharField(
        max_length=255, blank=True, null=True,)
    demand = models.CharField(
        max_length=255, blank=True, null=True,)
    rush_hour = models.CharField(
        max_length=255, blank=True, null=True,)
    peak = models.CharField(
        max_length=255, blank=True, null=True,)
    travel_time = models.CharField(
        max_length=255, blank=True, null=True,)
    crowd = models.CharField(
        max_length=255, blank=True, null=True,)
    safety = models.CharField(
        max_length=255, blank=True, null=True,)
    drive_safety = models.CharField(
        max_length=255, blank=True, null=True,)
    music = models.CharField(
        max_length=255, blank=True, null=True,)
    internet = models.CharField(
        max_length=255, blank=True, null=True,)

    def __str__(self):
        return "%s %s %s" % (self.stop_to, self.stop_from, self.amount)