from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView

from core_app import views
from core_app.views import (
    BaseView,
)
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# Simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', BaseView.as_view(), name='home'),
    
    path('api/board/', views.BoardViewSet.as_view({'get': 'index', 'post': 'create'}), name='board_view'),
    path('api/board/<int:board_id>/', views.BoardDetail.as_view({'get': 'index', 'put': 'update', 'delete': 'delete'}), name='board_single_view'),
    path('api/board/<int:board_id>/list/', views.ListViewSet.as_view({'get': 'index', 'post': 'create'}), name='list_view'),
    path('api/board/<int:board_id>/list/<int:list_id>', views.ListDetail.as_view({'get': 'index', 'put': 'update', 'delete': 'delete'}), name='list_detail'),
    path('api/board/<int:board_id>/list/<int:list_id>/card/', views.CardViewSet.as_view({'get': 'index', 'post': 'create'}), name='card_view'),
    path('api/board/<int:board_id>/list/<int:list_id>/card/<int:card_id>', views.CardDetail.as_view({'get': 'index', 'put': 'update'}), name='card_detail'),


    path('accounts/', include('rest_framework.urls')),
    path('api/signup/', views.SignUpView.as_view({'post' : 'signup'}), name='signup'),
    path('api/invited/signup/<str:token_id>/', views.InvitedSignUpView.as_view({'get' : 'check_token','post' : 'signup'}), name='invited_signup'),
    path('api/login/', views.LoginViewSet.as_view({'post' : 'login'}), name='login'),
    path('api/invite/', views.BoardInviteViewSet.as_view({'post' : 'invite'}), name='invite'),
    path('api/confirmation/<str:token_id>/', views.ConfirmInvitation.as_view({'get' : 'confirm'}), name='confirmation'),

    # Simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),

    # re_path('(.*)', TemplateView.as_view(template_name='base.html')),

]