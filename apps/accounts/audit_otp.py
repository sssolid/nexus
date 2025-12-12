from auditlog.registry import auditlog
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice

auditlog.register(TOTPDevice)
auditlog.register(StaticDevice)
