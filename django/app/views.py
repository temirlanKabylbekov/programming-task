from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.nest import NestValidationError, nester
from app.serializers import NestingSerializer


class NestingView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = NestingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = nester(serializer.validated_data['json_array'], serializer.validated_data['keys_path'])
            return Response(result)
        except NestValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
