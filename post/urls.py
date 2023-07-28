from django.urls import path
#from .views import post_list
from .views import post_detail
from .views import PostListView
from .views import post_share
from .views import post_comment

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    #path('', post_list, name='post_list'),
    path('<slug:slug>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
]