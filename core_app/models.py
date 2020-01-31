import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Board(models.Model):
    """ 
    Creating board model
    """

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=None, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    archive = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "({}) - {}".format(self.id, self.title)


class BoardList(models.Model):
    """ 
    Creating list model
    """

    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=None, blank=True)
    archive = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
 
    def __str__(self):
        return "{} - {}".format(self.id, self.title)


class Card(models.Model):
    """ 
    Creating card model
    """

    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=None, blank=True)
    date_created = models.DateField(default=timezone.now)
    archive = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    boardList = models.ForeignKey(BoardList, on_delete=models.CASCADE)

    def __str__(self):
        return "({}) - {}".format(self.id, self.title)


class Comment(models.Model):
    """
    Let the user put comments on cards
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)
    date_created = models.DateTimeField(default=timezone.now)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.id, self.comment)

class BoardMember(models.Model):
    """
    Let user add members and autorize them to view the board
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    activation = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)


class BoardInvite(models.Model):
    """
    Let the owner of the board invite new member to access the board
    """

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    member_email = models.EmailField(max_length=50, blank=True)
    archive = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4)

# localhost/invite/<token>

# get_invite object using token if activation is False


# class BoardInviteActiovation(BoardMixin, viewset)

#     def confirm_view(self, *args, **kwargs):
#         if self.request.user.is_authenticated():
#             invite = get_object_or_404(BoardInvite, token=<token>, activation=False)
#             invite.activation = True
#             invite.save()
#             self.add_member(self.request.user, invite.board) 
#         redirect(signup?token_id=<token>/)
    
# core/mixins.py
# class BoardMixin(object):

#     def add_member(self, email, board):
#         member = BoardMember.objects.get_or(user=user, board=board)
#         return member


# class SignupViewSet(BoardMixin)

#     def activate(self, args, )
#         username = self.request.data.get(usernaem)
#         passord - 
#         invite = InviteMember.objects.get(token=token)
#         invite.activation =True
#         invite.save()
#         new_member = user.objects.create_user(usernam=username, password=password)
#         self.add_member(member, invite.board)
#         return Response(status=200)