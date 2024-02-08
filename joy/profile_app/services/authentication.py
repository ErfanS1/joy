from typing import Optional

from profile_app.models.user import User


def authenticate(email: str, password: str) -> Optional[User]:
    try:
        user: User = User.objects.get(email=email)
    except User.DoesNotExist:
        return None

    if not user.check_password(password):
        return None

    return user
