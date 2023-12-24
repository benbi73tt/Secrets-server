# Create your views here.
import json

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, serializers
from rest_framework.response import Response

from ballroom.serializers import TrainerSerializer, TypeBallroomDancingSerializer, TeamSerializer, MemberSerializer, \
    CompetitionSerializer, CompetitionProgramSerializer, PointSerializer, EntrySerializer
from ballroom.models import Trainer, TypeBallroomDancing, Team, Member, Competition, CompetitionProgram, Point, Entry


class TrainerViewSet(viewsets.ModelViewSet):
    """ Сущность "Тренер" """
    serializer_class = TrainerSerializer
    queryset = Trainer.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = '__all__'
    ordering_fields = '__all__'


class TypeBallroomDancingViewSet(viewsets.ModelViewSet):
    """ Сущность "Тип бальных танцев" """
    serializer_class = TypeBallroomDancingSerializer
    queryset = TypeBallroomDancing.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = '__all__'
    ordering_fields = '__all__'


class TeamViewSet(viewsets.ModelViewSet):
    """ Сущность "Команда" """
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = '__all__'
    ordering_fields = '__all__'


class MemberViewSet(viewsets.ModelViewSet):
    """ Сущность "Участник" """
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['lastname', 'team', 'city', 'level']
    ordering_fields = '__all__'


class CompetitionViewSet(viewsets.ModelViewSet):
    """ Сущность "Соревнование" """
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = '__all__'
    ordering_fields = '__all__'


class CompetitionProgramViewSet(viewsets.ModelViewSet):
    """ Сущность "Программа соревнования" """
    serializer_class = CompetitionProgramSerializer
    queryset = CompetitionProgram.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = '__all__'
    ordering_fields = '__all__'


class PointViewSet(viewsets.ModelViewSet):
    """ Сущность "Баллы за соревнование" """
    serializer_class = PointSerializer
    queryset = Point.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = '__all__'
    ordering_fields = '__all__'


class ParamsViewSet(viewsets.ViewSet):
    """"""

    def set_params(self, request):
        params = request.data
        print(params)
        Entry.objects.create(
            title=params['title'],
            description=params['description'],
            date=params['date']
        )
        return Response({"params": params})

    def get_all_params(self, request):
        queryset = Entry.objects.all()
        serialized_q = json.loads(serialize('json', queryset))
        return JsonResponse({'data': serialized_q})

    def get_by_id(self, request, id):
        queryset = Entry.objects.filter(pk=id)
        serialized_q = json.loads(serialize('json', queryset))
        return JsonResponse({'data': serialized_q})
