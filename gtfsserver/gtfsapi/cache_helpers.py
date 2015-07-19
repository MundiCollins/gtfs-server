from django.core.cache import cache
from django.utils.encoding import force_text
import datetime

from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase, RetrieveSqlQueryKeyBit, ListSqlQueryKeyBit,
    PaginationKeyBit, QueryParamsKeyBit, UniqueMethodIdKeyBit,
    KwargsKeyBit
)


class UpdatedAtKeyBit(KeyBitBase):
    def get_data(self, **kwargs):
        feed_pk = kwargs['kwargs'].get('feed_pk', None)
        if not feed_pk:
            return ""

        key = '%s_feed_api_updated_at_timestamp' % feed_pk
        value = cache.get(key, None)
        if not value:
            value = datetime.datetime.utcnow()
            cache.set(key, value=value)
        return force_text(value)

#def calculate_cache_key_date(view_instance, view_method,
#                        request, args, kwargs):

class UpdatedAtDay(KeyBitBase):
    def get_data(self, **rkwargs):
        kwargs = rkwargs['kwargs']
        if kwargs.get('year', None):
            year, month, day = int(kwargs['year']), int(kwargs['month']), int(kwargs['day'])
            requested_date = datetime.date(year, month, day)
        else:
            requested_date = datetime.date.today()
        a = str(requested_date) + "__" + str(kwargs) + str(rkwargs['args'])
        a += str(rkwargs['request'].query_params)
        return a


class UpdatedAtDayForFeed(DefaultKeyConstructor):
    updated_at = UpdatedAtKeyBit()
    data_day = UpdatedAtDay()
    pagination = PaginationKeyBit()
    query = QueryParamsKeyBit()

class CustomObjectKeyConstructor(DefaultKeyConstructor):
    #retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = UpdatedAtKeyBit()
    #query = QueryParamsKeyBit()
    meth = UniqueMethodIdKeyBit()
    #kwargs = KwargsKeyBit()

class CustomListKeyConstructor(DefaultKeyConstructor):
    #list_sql = ListSqlQueryKeyBit()
    #pagination = PaginationKeyBit()
    updated_at = UpdatedAtKeyBit()
    #query = QueryParamsKeyBit()
    meth = UniqueMethodIdKeyBit()
    #kwargs = KwargsKeyBit()
