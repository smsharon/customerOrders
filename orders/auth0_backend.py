import requests
from jose import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework import authentication, exceptions


class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            # Cache JWKS to avoid hitting Auth0 every time
            jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks = cache.get("auth0_jwks")
            if not jwks:
                jwks = requests.get(jwks_url).json()
                cache.set("auth0_jwks", jwks, timeout=600)

            # Match key
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if not rsa_key:
                raise exceptions.AuthenticationFailed("Invalid token header.")

            # Decode & verify
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.API_IDENTIFIER,
                issuer=f"https://{settings.AUTH0_DOMAIN}/",
            )

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expired.")
        except jwt.JWTClaimsError:
            raise exceptions.AuthenticationFailed("Invalid claims.")
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid authentication token.")

        # Here you could map to Django user
        user = AnonymousUser()
        user.sub = payload.get("sub")  # attach sub for convenience
        return (user, None)
