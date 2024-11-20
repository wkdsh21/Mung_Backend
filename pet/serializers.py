from .models import *
from rest_framework import serializers


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = "__all__"  # __all__ 을 줄 경우, 모든 필드가 사용됨.
        # fields = ('id', 'created_at', 'title', 'category', 'star_rating',)  # req, res 시 사용되길 원하는 필드(컬럼)만 적어줘도 됨.


class MusicBodySerializer(serializers.Serializer):
    singer = serializers.CharField(help_text="가수명")
    title = serializers.CharField(help_text="곡 제목")
    category = serializers.ChoiceField(
        help_text="곡 범주", choices=("JPOP", "POP", "CLASSIC", "ETC")
    )
    star_rating = serializers.IntegerField(
        help_text="1~3 이내 지정 가능. 숫자가 클수록 좋아하는 곡"
    )
