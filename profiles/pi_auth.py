import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login
from django.db import models
from django.utils.timezone import now

# =========================
# CONFIG
# =========================
PI_API_KEY = os.getenv("PI_API_KEY")
PI_ENV = os.getenv("PI_ENV", "mainnet")

PI_VERIFY_URL = (
    "https://api.minepi.com/v2/me"
    if PI_ENV == "mainnet"
    else "https://api.testnet.minepi.com/v2/me"
)

# =========================
# USER MODEL
# =========================
class User(AbstractUser):
    pi_user_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    pi_username = models.CharField(max_length=100, null=True, blank=True)
    pi_wallet_address = models.CharField(max_length=200, null=True, blank=True)

    KYC_STATUS = (
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("rejected", "Rejected"),
    )
    kyc_status = models.CharField(max_length=20, choices=KYC_STATUS, default="pending")

    def is_pi_verified(self):
        return self.kyc_status == "verified"


# =========================
# PI TOKEN VERIFIER
# =========================
def verify_pi_token(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    r = requests.get(PI_VERIFY_URL, headers=headers, timeout=10)

    if r.status_code != 200:
        raise Exception("Invalid Pi token")

    return r.json()


# =========================
# AUTH ENDPOINT
# =========================
@csrf_exempt
def pi_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    token = data.get("accessToken")

    if not token:
        return JsonResponse({"error": "Missing token"}, status=400)

    try:
        pi_data = verify_pi_token(token)

        user, created = User.objects.get_or_create(
            pi_user_id=pi_data["uid"],
            defaults={
                "username": pi_data["username"],
                "pi_username": pi_data["username"],
                "kyc_status": "verified" if pi_data.get("kyc") else "pending",
                "last_login": now(),
            },
        )

        if not created:
            user.last_login = now()
            if pi_data.get("kyc"):
                user.kyc_status = "verified"
            user.save()

        login(request, user)

        return JsonResponse({
            "success": True,
            "user": {
                "pi_username": user.pi_username,
                "kyc_status": user.kyc_status
            }
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=401)
