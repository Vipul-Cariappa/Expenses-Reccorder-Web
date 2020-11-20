from api.views import bill_filter
from django.urls import path, re_path
from . import views

app_name = "api"
urlpatterns = [
    path('', views.index, name='home'),
    path('bills/<int:group_id>/', views.bill_list, name='bill'),
    path('bill/<int:bill_id>/', views.bill_detail, name='bill-detail'),
    path('create/bill/', views.bill_create, name='bill-create'),
    path('update/bill/<int:bill_id>/', views.bill_update, name='bill-update'),
    path('delete/bill/<int:bill_id>/', views.bill_delete, name='bill-delete'),
    path('categories/<int:group_id>/', views.category_list, name='category'),
    path('create/category/', views.category_create, name='category-create'),
    path('update/category/<int:category_id>/',
         views.category_update, name='category-update'),
    path('delete/category/<int:category_id>/',
         views.category_delete, name='category-delete'),
    path('groups/', views.group_list, name='group'),
    path('group/<int:group_id>/', views.group_detail, name='group-detail'),
    path('create/group/', views.group_create, name='group-create'),
    path('join/group/', views.group_join, name='group-join'),

    re_path(
        r'^bills/(?P<group_id>[0-9]+)/(?:year=(?P<year>[0-9]{4}))?&?(?:month=(?P<month>[0-9]+))?&?(?:day=(?P<day>[0-9]+))?&?(?:category=(?P<category>[0-9]+))?/', views.bill_filter, name="bill-filter"),
]
