"""
Defines the URL routes for this app.
"""

from .views import TrinityUserProfileView

from django.conf.urls import patterns, url

USERNAME_PATTERN = r'(?P<username>[\w.+-]+)'

urlpatterns = patterns(
    '',
    url(
        r'^api/user/v1/trinityprofile/' + USERNAME_PATTERN + '$',
        TrinityUserProfileView.as_view(),
        name="trinityuserprofile_api"
    ),
)