import base64
import pyotp

from robot.api.deco import keyword


@keyword("Generate 2FA Token")
def generate_auth_token(secret):
    encoded = base64.b64encode(base64.b64decode(secret))
    totp = pyotp.TOTP(encoded)
    token = str(totp.now())
    print("Current OTP:", token)
    return token