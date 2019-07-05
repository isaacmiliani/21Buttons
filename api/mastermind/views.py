from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from api.mastermind.serializers import UserSerializer, GroupSerializer, MastermindSerializer, MatchResumeSerializer
from .models import Mastermind, MatchResume
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from api.mastermind.tests.factories import MastermindFactory
from faker import Factory
import random
from datetime import datetime
from django.http import JsonResponse


@api_view(['GET'])
def get_all_games(request):

    try:
        game = Mastermind.objects.all()
    except Mastermind.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a all games
    if request.method == 'GET':
        queryset = Mastermind.objects.all().values()
        return JsonResponse({"games": list(queryset)})
    #return Response(json.dumps(game))


@api_view(['POST'])
def new_game(request):
    """Function to create a new game"""
    if request.method == 'POST':
        return post_new_game(request)
    
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'DELETE', 'POST'])
@permission_classes((IsAuthenticated,))
def get_game(request, pk):

    # get details of a single game
    if request.method == 'GET':
        return Response({})
    # delete a single game
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single game


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def post_new_game(request):
    user = request.user
    codes = ['G','R','B','Y']
    game_code = codes[random.randint(0, 3)]+'-'+codes[random.randint(0, 3)]+'-'+codes[random.randint(0, 3)]+'-'+codes[random.randint(0, 3)]
    data = {
            'match_time': datetime.now().time(),
            'name':'a name',
            'codeBreaker':str(user.id),
            'is_winner':False,
            'still_active':True,
            'game_code':game_code
        }
    faker = Factory.create()
    mastermind = Mastermind.objects.create(name=faker.name() + "'s Battle",codeBreaker=user,is_winner=False, still_active=True,game_code=game_code, match_time=datetime.now().time())
    return Response({'name': mastermind.name,'game_id':mastermind.id}, status=status.HTTP_201_CREATED)
        
        
def evaluate_code_by_position(code, game_code):
    code_response = ["*" for x in range(4)]
    for i, c in enumerate(code):
        if code[i] == game_code[i]:
             code_response[i] = 'R'
             
    return code_response
    
def evaluate_code_by_color(code, game_code, code_response):
    for i, c in enumerate(code):
        if code_response[i] == '*':
             for j, g in enumerate(game_code):
                 if code[i] == game_code[j]: 
                     code_response[i] = 'W'
                     game_code[j] = '*'
             
    return code_response

@api_view(['GET','POST','PUT'])
@permission_classes((IsAuthenticated,))
def post_code(request,pk):
    try:
        game = Mastermind.objects.get(pk=pk)
    except Mastermind.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if not game.still_active:
        return Response({'message':'This game is over'}, status=status.HTTP_201_CREATED)
    
    message = "Try again"
    if request.method == 'POST':
        code = request.data.get('code').split('-')
        game_code = game.game_code.split('-')
        code_r = evaluate_code_by_position(code, game_code)
        code_response = evaluate_code_by_color(code, game_code, code_r)
        match_resume = MatchResume.objects.create(code=request.data.get('code'), code_response='-'.join(code_response),match=game)
        if '-'.join(code_response) == 'R-R-R-R':
            message = "Winner"
            game.still_active = False
            game.is_winner = True
            a = datetime.strptime(str(game.match_time),"%H:%M:%S.%f") # convert string to time
            b = datetime.strptime(str(datetime.now().time()),"%H:%M:%S.%f")
            c = b - a
            game.match_time = datetime.strptime(str(c),"%H:%M:%S.%f")
            game.save()
            
        return Response({'message':message, 'code_response':'-'.join(code_response)}, status=status.HTTP_201_CREATED)
        
        
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    
class MastermindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = Mastermind.objects.all()
    serializer_class = MastermindSerializer
    
    
class MatchResumeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows games to be viewed or edited.
    """
    queryset = MatchResume.objects.all()
    serializer_class = MatchResumeSerializer
    
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
