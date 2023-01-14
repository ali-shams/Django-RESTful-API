from django.utils.translation import gettext_lazy as _
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status


def custom_exception_handler(exc, context):
    # breakpoint()
    response = exception_handler(exc, context)
    # if response is not None:
    #     response.data['status_code'] = response.status_code
        # response.data['message'] = response.data['detail']
    return response


class UniqueApiException(APIException):
    # public fields
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _('Bad Request.')
    default_code = 'bad_request'

    # custom fields
    detail = _('Unique Exception.')

    def __init__(self, field):
        # breakpoint()
        if field:
            detail = f"A user with that {field} already exists."
        # breakpoint()
        super().__init__(detail)
