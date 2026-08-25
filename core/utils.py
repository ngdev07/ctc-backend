from rest_framework.response import Response
from rest_framework import status

def get_limit(request , default = 10 , max_limit=100):

    limit = request.query_params.get("limit", default)

    try:
        limit = int (limit)

        if limit < 1:
            limit = default

        if limit > max_limit:
            limit = max_limit

    except (ValueError , TypeError):
        limit =  default

    return limit



def success_response(data = None , message="Succes." ,  status_code = status.HTTP_200_OK):

    return Response(
        {
            "success": True,
            "message" : message,
            "data" : data,
        },
        status=status_code
    )


def error_response(message="Une erreur est survenue.." , errors = None,  status_code = status.HTTP_400_BAD_REQUEST):
    
    return Response(
        {
            "success": False,
            "message" : message,
            "errors" : errors,
        },
        status=status_code
    )



