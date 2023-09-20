import rest_framework.pagination as pgn
from rest_framework import  generics

from .models import RSSUnsafe, Version, Clip
from .serializers import RSSUnsafeModelSerializer, RSSUnsafeSerializer

import IPython


class MyPagination(pgn.PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_query_param = 'num'
    page_size_query_param = 'size'


class RssPagination(generics.ListAPIView):
    queryset = RSSUnsafe.objects.all()
    serializer_class = RSSUnsafeModelSerializer
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # clip_fields = [field.name for field in Clip._meta.get_fields()]
        # single_column = self.request.query_params.get('column')
        version_name = self.request.query_params.get('version_name')  # Default to 'version_1'

        if version_name:
            version = Version.objects.get(version_name=version_name)
            queryset = queryset.filter(version=version)
        # if single_column:
        #     # IPython.embed()
        #
        #     if single_column in clip_fields:
        #         clip = Clip.objects.get(single_column=single_column)
        #         queryset = queryset.values_list(single_column, flat=True)

        return queryset
