from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from logger.models import NginxLog
from logger.serializers import NginxLogSerializer


class NginxLogsView(viewsets.ModelViewSet):
    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['request_date', 'http_method', 'response_code']
    search_fields = ['ip_address', 'uri', 'user_agent']

    def get_queryset(self):
        queryset = self.queryset.all()
        return queryset

    @action(methods=["GET"], detail=False, url_path='logs')
    def smart_list(self, request):
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
