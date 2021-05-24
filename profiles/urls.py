from django.urls import path, include
from .views import (
    my_profile_view,
    invites_received_view,
    profiles_list_view,
    invite_profiles_list_view,
    ProfileDetailView,
    ProfileListView,
    send_invitation,
    remove_from_connections,
    accept_invitation,
    reject_invitation,
    follow_unfollow_profile,
    

)

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListView.as_view(), name='all_profiles_view'),
    path('remove-connection/', remove_from_connections, name='remove_connection'),
    path('<slug>/', ProfileDetailView.as_view(), name='profile-detail_view'),
    path('my-invites/accept/', accept_invitation, name='accept_invite'),
    path('my-invites/reject/', reject_invitation, name='reject_invite'),
    path('switch_follow/', follow_unfollow_profile, name='follow-unfollow-view'),
    path('my-invites/', invites_received_view, name='my-invites-view'),
    path('all-profiles/', profiles_list_view, name='all_rofiles_view'),
    path('to-invite/', invite_profiles_list_view, name='invite_profiles_view'),
]
