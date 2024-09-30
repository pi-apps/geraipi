from django.db import models


class VoucherConfig(models.Model):
    generate_code = models.CharField(max_length=50)
    has_access_store = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
