from django.contrib.auth.models import User

from .models import BoardList, Board, Card
from core_app.serializers import BoardSerializer, ListSerializer, CardSerializer, UserSerializer, SignUpSerializer, LoginSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from core_app.models import Snippet
from core_app.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions, viewsets
from core_app.permissions import IsOwnerOrReadOnly

# samples
class UserList(generics.ListAPIView):
    """
    View the list of users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    View the single users
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_object(self, id):
        try:
            return Snippet.objects.get(id=id)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()

# login
# class loginView(APIView):




























# trello
# Boards
class BoardViewSet(viewsets.ViewSet):
    """
    List of Boards
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    content = {'404': 'not found'}
    empty_content = {'Board': 'is empty'}

    def index(self, *args, **kwargs):
        board = Board.objects.filter(owner=self.request.user, archive=True )
        if not board:
            return Response(self.empty_content, status=status.HTTP_404_NOT_FOUND)
        serializer = BoardSerializer(board, many=True)
        return Response(serializer.data)

    def create(self, *args, **kwargs):
        board = BoardSerializer(data=self.request.data)
        if board.is_valid():
            board.save(owner=self.request.user)
            return Response(board.data, status=status.HTTP_201_CREATED)
        return Response(board.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetail(viewsets.ViewSet):
    """
    ...
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    content = {'404': 'not found'}

    def index(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id, owner=self.request.user)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def update(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id, owner=self.request.user)
        serializer = BoardSerializer(board, data=self.request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id, owner=self.request.user)
        board.delete()


# Lists
class ListViewSet(viewsets.ViewSet):
    """
    Displays list of list
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    content = {'404': 'not found'}
    empty_content = {'List': 'is empty'}

    def index(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        list_obj = BoardList.objects.filter(board=board_id, board__owner=self.request.user, archive=True)
        if not list_obj:
            return Response(self.empty_content, status=status.HTTP_404_NOT_FOUND)
        serializer = ListSerializer(list_obj, many=True)
        return Response(serializer.data)

    def create(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id, owner=self.request.user)
        serializer = ListSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetail(viewsets.ViewSet):
    """
    ...
    """

    permission_classes = [permissions.IsAuthenticated]
    content = {'404': 'not found'}

    def index(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, board__owner=self.request.user, archive=True)
        serializer = ListSerializer(list_obj)
        return Response(serializer.data)

    def update(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, board__owner=self.request.user, archive=True)
        serializer = ListSerializer(list_obj, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, board__owner=self.request.user, archive=True)
        list_obj.delete()


# Cards
class CardViewSet(viewsets.ViewSet):
    """
    Displays list of cards
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    content = {'404': 'not found'}
    empty_content = {'Card': 'is empty'}

    def index(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = Card.objects.filter(boardList__id=list_id, boardList__board__owner=self.request.user, archive=True)
        if not list_obj:
            return Response(self.empty_content, status=status.HTTP_404_NOT_FOUND)
        serializer = CardSerializer(list_obj, many=True)
        return Response(serializer.data)

    def create(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, board__owner=self.request.user)
        serializer = CardSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(boardList=list_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetail(viewsets.ViewSet):
    """
    Show the 
    """

    permission_classes = [permissions.IsAuthenticated]
    content = {'404': 'not found'}

    def index(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_obj = get_object_or_404(Card, id=card_id, boardList__board__owner=self.request.user, archive=True)
        serializer = ListSerializer(card_obj)
        return Response(serializer.data)

    def update(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_obj = get_object_or_404(Card, id=card_id, boardList__board__owner=self.request.user, archive=True)
        serializer = ListSerializer(card_obj, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_obj = get_object_or_404(Card, id=card_id, boardList__board__owner=self.request.user, archive=True)
        card_obj.delete()


class SignUpView(viewsets.ViewSet):
    """
    Allow the user to login
    """

    serializer_class = SignUpSerializer

    def signup(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.data)


class LoginViewSet(viewsets.ViewSet):
    """
    Login with token
    """
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    def login(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            user = User.objects.get(username=self.request.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token':token.key,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)