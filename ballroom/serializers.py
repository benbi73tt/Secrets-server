from rest_framework import serializers

from ballroom.models import Trainer, TypeBallroomDancing, Team, Member, Competition, CompetitionProgram, Point, User, \
    Entry


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        ref_name = "User 1"
        model = User
        fields = ('id', 'full_name', 'username', 'first_name', 'last_name', 'email', 'sur_name')


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = ('__all__')


class TypeBallroomDancingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeBallroomDancing
        fields = ('__all__')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('__all__')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('__all__')


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ('__all__')


class CompetitionProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionProgram
        fields = ('__all__')


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('__all__')


class EntrySerializer(serializers.Serializer):
    title = serializers.CharField(label='Имя ребенка')
    description = serializers.CharField(label='Код')
    date = serializers.CharField(label='Продолжительность жизни кода(в секундах)')
