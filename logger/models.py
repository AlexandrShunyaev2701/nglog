from django.db import models


class NginxLog(models.Model):
    ip_address = models.GenericIPAddressField()
    request_date = models.DateTimeField()
    remote_user = models.CharField(max_length=255, null=True, blank=True, default="-")
    http_method = models.CharField(max_length=10)
    uri = models.CharField(max_length=2048)
    protocol = models.CharField(max_length=20, default="HTTP/1.1")
    response_code = models.IntegerField()
    response_size = models.BigIntegerField()
    referrer = models.CharField(max_length=2048, null=True, blank=True, default="-")
    user_agent = models.CharField(max_length=1024, null=True, blank=True)
