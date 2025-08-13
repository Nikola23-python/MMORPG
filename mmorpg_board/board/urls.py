from django.urls import path

from board.views import PostsList, PostDetail, PostCreate, ConfirmUser

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_edit'),
    path('user/confirm/', ConfirmUser.as_view(), name='user_confirm'),
]