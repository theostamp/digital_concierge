from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vote, VoteAnswer, VoteOption
from .serializers import VoteSerializer, VoteAnswerSerializer, VoteOptionResultSerializer
from .permissions import IsManagerOrReadOnly
from django.utils.timezone import now
from django.db.models import Count

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsManagerOrReadOnly]

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "request": self.request}

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        vote = self.get_object()
        option_id = request.data.get('option')
        if not option_id:
            return Response({'error': 'Missing option ID'}, status=400)
        try:
            option = VoteOption.objects.get(id=option_id, vote=vote)
            answer, created = VoteAnswer.objects.get_or_create(user=request.user, option=option)
            if not created:
                return Response({'detail': 'Already voted.'}, status=400)
            return Response(VoteAnswerSerializer(answer).data)
        except VoteOption.DoesNotExist:
            return Response({'error': 'Invalid option.'}, status=404)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def results(self, request, pk=None):
        vote = self.get_object()

        if vote.expires_at > now():
            return Response(
                {'detail': 'Τα αποτελέσματα θα είναι διαθέσιμα μετά τη λήξη της ψηφοφορίας.'},
                status=403
            )

        options = vote.options.annotate(votes_count=Count('answers')).all()
        total_votes = sum(opt.votes_count for opt in options)

        data = []
        for opt in options:
            percentage = (opt.votes_count / total_votes * 100) if total_votes > 0 else 0
            data.append({
                'id': opt.id,
                'text': opt.text,
                'votes_count': opt.votes_count,
                'percentage': round(percentage, 2)
            })

        return Response({
            'vote_id': vote.id,
            'title': vote.title,
            'results': data,
            'total_votes': total_votes
        })