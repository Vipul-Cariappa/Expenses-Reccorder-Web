from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.index, name='home'),
    path('add-bill/<int:group_id>/', views.bill_new, name='bill-add'),
    path('group-error/', views.error, name='group-error'),
    path('group/<int:group_id>/', views.view_bill, name='group'),
    path('bill/<int:bill_id>/', views.each_bill, name='bill'),
    path('bill-edit/<int:bill_id>/', views.edit_bill, name='bill-edit'),
    path('bill-delete/<int:bill_id>/', views.bill_delete, name='bill-delete'),
    path('add-category/<int:group_id>/', views.category_new, name='category-add'),
    path('category-management/<int:group_id>/', views.category_manage, name='category-manage'),
    path('category-delete/<int:category_id>/', views.category_delete, name='category-delete'),
    path('group-management/', views.group_management, name='group-manage'),
    path('group-leave/<int:group_id>/', views.group_leave, name='group-leave'),
    path('group-leave/<int:group_id>/<int:user_id>/', views.group_leave_user, name='group-deleteuser'),
    path('group-delete/<int:group_id>/', views.group_delete, name='group-delete'),


    path('join-group/', views.group_join, name="group-join"),
    path('add-group/', views.group_new, name="group-add"),

]