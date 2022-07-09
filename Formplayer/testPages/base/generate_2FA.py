import base64
import pyotp

""""Generates two factor authorization otp token"""


def generate_auth_token(secret):
    encoded_secret = base64.b64encode(base64.b64decode(secret))
    totp = pyotp.TOTP(encoded_secret)
    token = str(totp.now())
    print("Current OTP:", token)
    return token
