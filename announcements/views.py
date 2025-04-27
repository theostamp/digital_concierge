# 📄 announcements/views.py

from rest_framework import viewsets
from .models import Announcement
from .serializers import AnnouncementSerializer
from .permissions import IsManagerOrReadOnly

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsManagerOrReadOnly]
