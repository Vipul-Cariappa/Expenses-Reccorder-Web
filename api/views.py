from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response

from record.models import Bill, Category, Group
from .serializers import BillSerializer, CategorySerializer, GroupSerializer, UserSerializer

# Create your views here.


@api_view(['GET'])
def index(request):
    context = {
        "List Bill": "api/bills/<int:pk>/",
        "Filter Bill": "api/bills/<int:pk>/<option=value>",
        "Detail Bill": "api/bill/<int:pk>/",
        "Create Bill": "api/create/bill/",
        "Update Bill": "api/update/bill/<int:pk>/",
        "Delete Bill": "api/delete/bill/<int:pk>/",

        "List Category": "api/categories/<int:pk>/",
        "Create Category": "api/create/category/",
        "Update Category": "api/update/category/<int:pk>/",
        "Delete Category": "api/delete/category/<int:pk>/",

        "List Group": "api/groups/",
        "Detail Group": "api/group/<int:pk>/",
        "Create Group": "api/create/group/",
        "Join Group": "api/join/group/",
        "Delete Group": "group-delete/<int:pk>/",
        "Group Leave": "group-leave/<int:pk>/",
        "Group User Remove": "group-leave/<int:pk>/<int:pk>/",

    }
    return Response(context)


@api_view(['GET'])
def bill_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    active_user = request.user

    if active_user in group.users.all():
        obj = Bill.objects.filter(group=group).order_by("-date")
        serializer = BillSerializer(obj, many=True)
        return Response(serializer.data)

    # else
    return Response({'detail': 'Not found.'})


@api_view(['GET'])
def bill_filter(request, group_id, *arges, **kwargs):
    group = get_object_or_404(Group, pk=group_id)
    active_user = request.user

    if active_user in group.users.all():
        obj = Bill.objects.filter(group=group).order_by("-date")

        if kwargs["year"] != None:
            obj = obj.filter(date__year=int(kwargs["year"]))
        if kwargs["month"] != None:
            obj = obj.filter(date__month=int(kwargs["month"]))
        if kwargs["day"] != None:
            obj = obj.filter(date__day=int(kwargs["day"]))
        if kwargs["category"] != None:
            obj = obj.filter(category=int(kwargs["category"]))

        serializer = BillSerializer(obj, many=True)
        return Response(serializer.data)

    # else
    return Response({'detail': 'Not found.'})


@api_view(['GET'])
def bill_detail(request, bill_id):
    active_user = request.user
    obj = get_object_or_404(Bill, pk=bill_id)

    if active_user in obj.group.users.all():
        serializer = BillSerializer(obj, many=False)
        return Response(serializer.data)

    # else
    return Response({'detail': 'Not found.'})


@api_view(['POST'])
def bill_create(request):
    active_user = request.user
    try:
        request.data._mutable = True
    except:
        pass

    try:
        category = request.data["category"]
        group = request.data["group"]
    except KeyError:
        return Response({'error': 'data not valid'})
    else:
        category = get_object_or_404(Category, pk=category)
        group = get_object_or_404(Group, pk=group)
        request.data["edited"] = active_user.id

    if active_user in group.users.all() and category.group == group:
        serializer = BillSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(category=category, group=group)
            return Response(serializer.data)

        # else
        return Response({'error': 'data not valid'})

    # else
    return Response({'detail': 'Not found.'})


@api_view(['POST'])
def bill_update(request, bill_id):
    active_user = request.user
    try:
        request.data._mutable = True
    except:
        pass

    try:
        category = request.data["category"]
        group = request.data["group"]
    except KeyError:
        return Response({'error': 'data not valid'})
    else:
        category = get_object_or_404(Category, pk=category)
        group = get_object_or_404(Group, pk=group)
        request.data["edited"] = active_user.id
        obj = get_object_or_404(Bill, pk=bill_id)

    if active_user in group.users.all() and category.group == group:
        serializer = BillSerializer(data=request.data, instance=obj)

        if serializer.is_valid():
            serializer.save(category=category, group=group)
            return Response(serializer.data)

        # else
        return Response({'error': 'data not valid'})

    # else
    return Response({'detail': 'Not found.'})


@api_view(['DELETE'])
def bill_delete(request, bill_id):
    active_user = request.user
    obj = get_object_or_404(Bill, pk=bill_id)

    if active_user in obj.group.users.all():
        obj.delete()
        return Response('Item succsesfully delete!')

    # else
    return Response({'detail': 'Not found.'})


@api_view(['GET'])
def category_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    active_user = request.user

    if active_user in group.users.all():
        obj = Category.objects.filter(group=group)
        serializer = CategorySerializer(obj, many=True)
        return Response(serializer.data)

    # else
    return Response({'detail': 'Not found.'})


@api_view(['POST'])
def category_create(request):
    active_user = request.user
    group = get_object_or_404(Group, pk=request.data["group"])

    if active_user in group.users.all():
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():

            try:
                serializer.save(group=group)
            except IntegrityError:
                return Response({'error': 'Category with same name exists'})

            return Response(serializer.data)

        # else
        return Response({'error': 'data not valid'})

    # else
    return Response({'detail': 'Not found.'})


@api_view(['POST'])
def category_update(request, category_id):
    active_user = request.user
    group = get_object_or_404(Group, pk=request.data["group"])
    obj = get_object_or_404(Category, pk=category_id)

    if active_user in group.users.all() and obj.group == group:
        serializer = CategorySerializer(data=request.data, instance=obj)

        if serializer.is_valid():
            try:
                serializer.save(group=group)
            except IntegrityError:
                return Response({'error': 'Category with same name exists'})

            return Response(serializer.data)

        # else
        return Response({'error': 'data not valid'})

    # else
    return Response({'detail': 'Not found.'})


@api_view(['DELETE'])
def category_delete(request, category_id):
    active_user = request.user
    obj = get_object_or_404(Category, pk=category_id)

    if active_user in obj.group.users.all():
        obj.delete()
        return Response('Item succsesfully delete!')

    # else
    return Response({'detail': 'Not found.'})


@api_view(['GET'])
def group_list(request):
    active_user = request.user

    obj = Group.objects.filter(users=active_user)
    serializer = GroupSerializer(obj, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def group_detail(request, group_id):
    active_user = request.user

    obj = get_object_or_404(Group, pk=group_id, users=active_user)
    serializer = GroupSerializer(obj, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def group_create(request):
    active_user = request.user
    try:
        name = request.data["name"]
        password = request.data["password"]
    except KeyError:
        return Response({'detail': 'Not found.'})

    try:
        s = Group(
            name=name,
            password=password,
            admin=active_user
        )
        s.save()
        s.users.add(active_user)
        s.save
    except IntegrityError:
        return Response({'error': "Group Name Taken"})

    serializer = GroupSerializer(s, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def group_join(request):
    active_user = request.user
    try:
        name = request.data["name"]
        password = request.data["password"]
    except KeyError:
        return Response({'detail': 'Not found.'})

    obj = get_object_or_404(Group, name=name)
    if obj.password == password:
        obj.users.add(active_user)
        obj.save()

        serializer = GroupSerializer(obj, many=False)
        return Response(serializer.data)

    return Response({'error': "Password Miss Match"})
