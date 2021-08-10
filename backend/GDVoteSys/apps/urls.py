from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'get_year', views.QueryYear.as_view()),
    url(r'get_meeting/(?P<year>\d{4})', views.QueryMeeting.as_view()),
    url(r'get_shareholder', views.AddMeeting.as_view()),
    url(r'add_meeting', views.AddMeeting.as_view()),
    url(r'get_detail/(?P<year>\d{4})/(?P<meeting_name>\w+)', views.QueryDetail.as_view()),
    url(r'update/$', views.UpdateMeeting.as_view()),
    url(r'api/posts/upload', views.Upload.as_view()),
    url(r'loadall', views.LoadAll.as_view()),
    url(r'download/result', views.Download.as_view()),
    url(r'delete/$', views.Delete.as_view()),
    url(r'login', views.Login.as_view()),
    url(r'current', views.Current.as_view()),
    url(r'result/(?P<year>\d{4})/(?P<meeting_name>\w+)', views.Result.as_view()),
    url(r'motion/(?P<year>\d{4})/(?P<meeting_name>\w+)', views.Motion.as_view()),
    url(r'record', views.Record.as_view()),
    url(r'update_meeting', views.UpdateAnnualMeeting.as_view()),
    url(r'meeting/update', views.UpdateAnnualMeeting.as_view()),
    url(r'meeting/motion', views.UpdateAnnualMeeting.as_view()),
    url(r'upload',views.Upload.as_view()),
    url(r'teller', views.Teller.as_view()),
]