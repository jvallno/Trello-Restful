from .models import BoardMember, Board
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404


class MembersMixIn:
    """
    Member MixIn
    """
    
    def dispatch(self, *args, **kwargs):
        board_id = kwargs.get('board_id')
        if BoardMember.objects.filter(user=self.request.user, board=board_id, activation = True) or Board.objects.filter(owner=self.request.user, archive=False, id=board_id):
            return super().dispatch(self.request, *args, **kwargs)
        raise Http404