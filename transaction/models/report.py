from django.db import models
from transaction.models.user import TransactionUser
from transaction.models.user_store import TransactionUserStore
from transaction.models.cart_item import CartItem
from transaction.models.report_image import ReportImage


class Report(models.Model):
    user = models.ForeignKey(TransactionUser, on_delete=models.CASCADE, related_name="transaction_report_user")
    vendor = models.ForeignKey(TransactionUserStore, on_delete=models.CASCADE, related_name="transaction_report_vendor")
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name="transaction_report_cart_item")
    image = models.ManyToManyField(ReportImage, related_name="transaction_report_images")
    catatan = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.user
