from django.urls import path

from board.views import PostsList, PostDetail, PostCreate, ConfirmUser, ProfileView, comment_accept, comment_delete

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_edit'),
    path('user/confirm/', ConfirmUser.as_view(), name='user_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('comment/<int:pk>/accept/', comment_accept, name='comment_accept'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
]