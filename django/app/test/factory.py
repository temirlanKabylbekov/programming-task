from mixer.backend.django import mixer

USER_PASSWORD = '12345'


class Factory:
    @classmethod
    def user(cls, **kwargs):
        user = mixer.blend('auth.User', **kwargs)
        user.set_password(USER_PASSWORD)
        user.save()
        return user
