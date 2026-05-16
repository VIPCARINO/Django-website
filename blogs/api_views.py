from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlogSerializer

SECRET_API_KEY = "my_secret_key"

@api_view(["POST"])
def create_blog(request):

    api_key = request.headers.get(
        "X-API-KEY"
    )

    if api_key != SECRET_API_KEY:

        return Response(
            {"error": "Unauthorized"},
            status=401
        )

    serializer = BlogSerializer(
        data=request.data
    )

    if serializer.is_valid():

        blog = serializer.save()

        return Response({
            "success": True
        })

    return Response(
        serializer.errors,
        status=400
    )