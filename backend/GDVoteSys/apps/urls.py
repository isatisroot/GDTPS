from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'captcha/(?P<uuid>.*)/$',views.Regiter.as_view()),
    # url(r'register/$', views.Regiter.as_view()),
    url(r'get_year', views.QueryYear.as_view()),
    url(r'get_meeting/(?P<year>\d{4})', views.QueryMeeting.as_view()),
    url(r'get_shareholder', views.AddMeeting.as_view()),
    url(r'add_meeting', views.AddMeeting.as_view()),
    url(r'get_detail/(?P<year>\d{4})/(?P<meeting_name>\w+)', views.QueryDetail.as_view()),
    url(r'update', views.UpdateMeeting.as_view()),
    url(r'api/posts/upload', views.Upload.as_view()),
    # url(r'add/', views.Add.as_view()),
]