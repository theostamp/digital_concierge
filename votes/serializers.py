from rest_framework import serializers
from .models import Vote, VoteOption, VoteAnswer
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class VoteOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteOption
        fields = ['id', 'text']

class VoteSerializer(serializers.ModelSerializer):
    options = VoteOptionSerializer(many=True)
    has_voted = serializers.SerializerMethodField()
    voted_option_id = serializers.SerializerMethodField()

    class Meta:
        model = Vote
        fields = ['id', 'title', 'description', 'expires_at', 'building', 'options', 'has_voted', 'voted_option_id']

    def get_has_voted(self, obj):
        user = self.context['request'].user
        return VoteAnswer.objects.filter(option__vote=obj, user=user).exists()

    def get_voted_option_id(self, obj):
        user = self.context['request'].user
        answer = VoteAnswer.objects.filter(option__vote=obj, user=user).first()
        return answer.option.id if answer else None

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        vote = Vote.objects.create(**validated_data)
        for option_data in options_data:
            VoteOption.objects.create(vote=vote, **option_data)
        return vote

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.expires_at = validated_data.get('expires_at', instance.expires_at)
        instance.save()
        if options_data:
            instance.options.all().delete()
            for option_data in options_data:
                VoteOption.objects.create(vote=instance, **option_data)
        return instance

class VoteAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteAnswer
        fields = ['id', 'option', 'user', 'voted_at']
        read_only_fields = ['user', 'voted_at']
        
class VoteOptionResultSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField()

    class Meta:
        model = VoteOption
        fields = ['id', 'text', 'votes_count']