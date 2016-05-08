from django.core import serializers
from django import http


class AJAXListMixin(object):
    def dispatch(self, request, *args, **kwargs):
        #if not request.is_ajax():
        #    raise http.Http404("This is an ajax view, friend.")
        return super(AJAXListMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(AJAXListMixin, self).get_queryset()

        if self.request.GET.get('inbound_status') and self.request.GET.get('corridor'):
            inbound_status = self.request.GET.get('inbound_status')
            corridor = self.request.GET.get('corridor')
            regex = r"^{}\d{}".format(corridor, inbound_status)

            queryset = queryset.filter(stop_id__regex=regex)

        return queryset.order_by('name')

    def get(self, request, *args, **kwargs):
        return http.HttpResponse(serializers.serialize('json', self.get_queryset()))
