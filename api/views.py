
from rest_framework.views import APIView
from rest_framework.response import Response
from announcements.models import Announcement
from requests.models import Request
# Ensure the votes app is installed and the Vote model exists
try:
    from votes.models import Vote
except ImportError:
    raise ImportError("The 'votes' app or 'Vote' model could not be found. Ensure the app is installed and the model exists.")
from announcements.serializers import AnnouncementSerializer
from announcements.serializers import RequestSerializer  # Update this import to the correct module
from votes.serializers import VoteSerializer


class FeedView(APIView):
    def get(self, request):
        announcements = Announcement.objects.order_by('-created_at')[:5]
        requests = Request.objects.filter(status='open').order_by('-created_at')[:5]
        votes = Vote.objects.filter(active=True).order_by('-created_at')[:5]

        return Response({
            'announcements': AnnouncementSerializer(announcements, many=True).data,
            'requests': RequestSerializer(requests, many=True).data,
            'votes': VoteSerializer(votes, many=True).data
        })
