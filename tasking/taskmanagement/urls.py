from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth import logout

#from ledger.accounts.views import logout 
#from ledger.urls import urlpatterns as ledger_patterns
from taskmanagement import views
from taskmanagement import view_file
from taskmanagement import api

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home_page'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^logout/$', logout, name='logout'),
    url(r'^new-task/', views.NewTask.as_view(),  name='new_task'),
    url(r'^edit-task/(?P<pk>[0-9]+)/', views.EditTask.as_view(),  name='edit_task'),
    url(r'^assign-task/(?P<pk>[0-9]+)/', views.AssignTask.as_view(),  name='assign_task'),
    #url(r'^assign-task-bulk/', views.AssignTaskBulk.as_view(),  name='assign_task_bulk'),
    url(r'^my-task-assignments/', views.MyTaskAssignments.as_view(),  name='my_task_assignments'),
    url(r'^my-assigned-tasks/', views.MyAssignedTasks.as_view(),  name='my_assigned_tasks'),
    url(r'^task-group/(?P<group_type>[0-9]+)/(?P<pk>[0-9]+)/', views.GroupTasks.as_view(),  name='group_tasks'),
    url(r'^view-task/(?P<pk>[0-9]+)/$', views.ViewTask.as_view(),  name='view_task'),
    url(r'^api/search-pg/', api.search_pg, name='search_pg'),
    url(r'^api/create_task_comment/', api.create_task_comment, name='create_task_comment'),
    url(r'^private-media/view/(?P<file_id>\d+)-file.(?P<extension>\w\w\w)$', view_file.getTCFile, name='view_private_file'),
    url(r'^private-media/view/(?P<file_id>\d+)-file.(?P<extension>\w\w\w\w)$', view_file.getTCFile, name='view_private_file2')


]

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

