from django.contrib import admin
from .models import Board, BoardList, Card, BoardMember, Comment, BoardInvite

admin.site.register(Board)
admin.site.register(BoardList)
admin.site.register(Card)
admin.site.register(BoardMember)
admin.site.register(Comment)
admin.site.register(BoardInvite)