from django.core.cache import cache
from django.utils.encoding import force_text

from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase, RetrieveSqlQueryKeyBit, ListSqlQueryKeyBit,
    PaginationKeyBit, QueryParamsKeyBit, UniqueMethodIdKeyBit,
    KwargsKeyBit
)


class UpdatedAtKeyBit(KeyBitBase):
    def get_data(self, **kwargs):
        feed_pk = kwargs['kwargs'].get('feed_pk', '0')
        key = '%s_feed_api_updated_at_timestamp' % feed_pk
        value = cache.get(key, None)
        if not value:
            value = datetime.datetime.utcnow()
            cache.set(key, value=value)
        return force_text(value)

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
