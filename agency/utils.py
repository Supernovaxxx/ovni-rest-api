def get_agency_for_user(user, actions=('manage',)):
    return get_agencies_for_user(user, actions).first()


def get_agencies_for_user(user, actions=('manage',)):
    from .models import Agency

    return Agency.objects.for_user(user, actions)







