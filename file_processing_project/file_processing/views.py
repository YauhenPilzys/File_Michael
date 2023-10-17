from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer
from .tasks import process_file

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        file = self.get_object()
        if not file.processed:
            process_file.delay(file.id)
            return Response({'message': 'File processing started.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'File already processed.'}, status=status.HTTP_400_BAD_REQUEST)