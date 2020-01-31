import uuid

from django.http import Http404
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from core_app.permissions import IsOwnerOrReadOnly
from core_app.serializers import BoardSerializer, ListSerializer, CardSerializer, UserSerializer, SignUpSerializer, BoardInviteSerializer

from .mixin import MembersMixIn
from .models import BoardList, Board, Card, BoardInvite, BoardMember



class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class BaseView(TemplateView):
    template_name = 'base.html'

# Boards
class BoardViewSet(viewsets.ViewSet):
    """
    Display the list of boards
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    def index(self, *args, **kwargs):
        board = Board.objects.filter(owner=self.request.user, archive=False )
        serializer = BoardSerializer(board, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, *args, **kwargs):
        board = BoardSerializer(data=self.request.data)
        if board.is_valid():
            board.save(owner=self.request.user)
            return Response(board.data, status=status.HTTP_201_CREATED)
        return Response(board.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetail(MembersMixIn, viewsets.ViewSet):
    """
    Display the board in single view
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def index(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id)
        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id)
        serializer = BoardSerializer(board, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id)
        board.delete()
        return Response(status=status.HTTP_200_OK)


# Lists
class ListViewSet(MembersMixIn, viewsets.ViewSet):
    """
    Displays the set of list
    """
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def index(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        list_obj = BoardList.objects.filter(board=board_id, archive=False)
        serializer = ListSerializer(list_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = get_object_or_404(Board, id=board_id, owner=self.request.user)
        serializer = ListSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetail(MembersMixIn, viewsets.ViewSet):
    """
    Display the list in single view
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def index(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, archive=False)
        serializer = ListSerializer(list_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, archive=False)
        serializer = ListSerializer(list_obj, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id, archive=False)
        list_obj.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


# Cards
class CardViewSet(MembersMixIn, viewsets.ViewSet):
    """
    Displays list of cards
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def index(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = Card.objects.filter(boardList__id=list_id, archive=False)
        serializer = CardSerializer(list_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, *args, **kwargs):
        list_id = kwargs.get('list_id')
        list_obj = get_object_or_404(BoardList, id=list_id)
        serializer = CardSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save(boardList=list_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetail(MembersMixIn, viewsets.ViewSet):
    """
    Display the card in single view
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def index(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_obj = get_object_or_404(Card, id=card_id, archive=False)
        serializer = CardSerializer(card_obj)
        return Response(serializer.data)

    def update(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_obj = get_object_or_404(Card, id=card_id, archive=False)
        serializer = CardSerializer(card_obj, data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        card_id = kwargs.get('card_id')
        card_obj = get_object_or_404(Card, id=card_id)
        card_obj.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class SignUpView(viewsets.ViewSet):
    """
    Allow the user to login
    """

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    

    def signup(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """
    Login with token
    """
    
    content_error = 'Your username or password is incorrect!'
    serializer_class = UserSerializer
    
    def login(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            username = self.request.data['username']
            password = self.request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token':token.key,}, status=status.HTTP_200_OK)
        return Response(self.content_error, status=status.HTTP_400_BAD_REQUEST)


class BoardInviteViewSet(viewsets.ViewSet):
    """
    Enable the owner to invite member to existing board
    """

    permission_classes = [permissions.IsAuthenticated]
    subject = 'Trello Confirmation'

    def invite(self, *args, **kwargs):
        # board_id = kwargs.get('board_id')
        # board = Board.objects.get(id=2)
        email = BoardInviteSerializer(data=self.request.data)
        user = Board.objects.get(id=2)
        if email.is_valid():
            subject, from_email, to = self.subject, settings.DEFAULT_FROM_EMAIL, email.data['member_email']
            BoardInvite.objects.get_or_create(board=user, member_email=email.data['member_email'])
            token = BoardInvite.objects.get(member_email=self.request.data['member_email'])
            text_content = 'This is an important message.'
            html_content = '<p>Click the button to confirm the invitation</p><br><a href="' + self.request.build_absolute_uri('/confirmation/')+str(token.token) + '" class="btn btn-danger">Confirm</a>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response(email.data, status=status.HTTP_200_OK)
        return Response(email.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmInvitation(viewsets.ViewSet):
    """
    Let the user confirm the invitation
    """

    success = 'You have confirmed the invitation!'
    template_name = 'board_single_view'
    invited_template_name = 'invited_signup'

    def confirm(self, *args, **kwargs):
        token_id = kwargs.get('token_id')
        invited_user = BoardInvite.objects.get()
        if str(invited_user.token) == token_id:
            token_uuid = uuid.UUID(token_id).hex
            user = BoardInvite.objects.get(token=token_uuid)
            check_user = User.objects.filter(email=user.member_email).exists()
            if check_user:
                user = User.objects.get(email=invited_user.member_email)
                create_member = BoardMember.objects.get_or_create(user=user, board=invited_user.board, activation=True)
                invited_user.archive = True
                invited_user.save()
                return redirect(self.template_name, invited_user.board.id)
            return redirect(self.invited_template_name, token_id)
        return Response(status=status.HTTP_404_NOT_FOUND)


class InvitedSignUpView(viewsets.ViewSet):
    """
    Allow the user to login
    """

    serializer_class = SignUpSerializer
    template_name = 'board_single_view'

    def check_token(self, *args, **kwargs):
        token_id = kwargs.get('token_id')
        invited_user = BoardInvite.objects.get()
        if str(invited_user.token) == token_id:
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def signup(self, *args, **kwargs):
        token_id = kwargs.get('token_id')
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = get_object_or_404(User, email=email)
            invited = get_object_or_404(BoardInvite, member_email=email)
            create_member = BoardMember.objects.get_or_create(user=user, board=invited.board, activation=True)
            invited.archive = True
            invited.save()
            serializer.save()
            return redirect(self.template_name, invited.board.id)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)