from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.db import IntegrityError
from django.contrib import messages
from .forms import BillForm, CategoryForm, GroupForm, JoinGroupForm
from .models import Bill, Category, Group
from .function import get_groups
from django.contrib.auth.models import User
from datetime import date
from My_Bills.settings import _IP_ADDR, _PORT


# Create your views here.
def index(request):
    """
    Home Page
    """
    active_user = request.user  # Get User
    context = {}

    try:
        # Try to get list of all groups user belongs to
        groups = Group.objects.filter(users=active_user)
    except TypeError:
        pass
    else:
        context["profile_list"] = groups

    return render(request, 'record/home.html', context)


def error(request):
    """
    Error Page: If any error is encountered in authentication it is redirected here.
    If someone is trying to access something he does not have permission to.
    """
    active_user = request.user  # Get User
    context = {}

    try:
        # Try to get list of all groups user belongs to
        groups = Group.objects.filter(users=active_user)
    except TypeError:
        pass
    else:
        context["profile_list"] = groups

    return render(request, 'record/error.html', context)


@login_required
def bill_new(request, group_id):
    """
    Add new Bill

    Args:
        group_id (int): id of group
    """

    active_user = request.user
    group = get_object_or_404(Group, pk=group_id)

    if active_user in group.users.all():
        if request.method == "POST":
            form = BillForm(request.POST, group_name=group)
            if form.is_valid():
                post = form.save(commit=False)
                post.edited = active_user
                post.group = group
                post.save()

                return redirect('home:group', group_id)

        else:
            form = BillForm(group_name=group)

        context = {
            'form': form,
            'group_id': group_id,
            'profile_list': get_groups(active_user)
        }

        return render(request, 'record/bill.html', context)

    # else
    return redirect('home:group-error')


@login_required
def category_new(request, group_id):
    """
    Add new category to specified group

    Args:
        group_id (int): id of group
    """

    active_user = request.user
    group = get_object_or_404(Group, pk=group_id)

    if active_user in group.users.all():
        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.group = group

                try:
                    post.save()
                except IntegrityError:
                    messages.success(request, f"This Category already exists!")
                    return redirect('home:category-add', group_id)
                else:
                    messages.success(request, f"New Category Created!")
                    return redirect('home:bill-add', group_id)

        else:
            form = CategoryForm()

        context = {
            'form': form,
            'group_id': group_id,
            'profile_list': get_groups(active_user)
        }

        return render(request, 'record/category.html', context)

    # else
    return redirect('home:group-error')


@login_required
def view_bill(request, group_id):
    """
    To view list of all bills

    Args:
        group_id (int): id of group
    """

    group = get_object_or_404(Group, pk=group_id)
    cate = Category.objects.filter(group=group)
    active_user = request.user

    year = [
        d.year for d in Bill.objects.filter(
            group=group
        ).dates(
            'date', 'year'
        )
    ]

    context = {
        'group': group,
        'group_id': group_id,
        'category': cate,
        'year': year,
        'profile_list': get_groups(active_user),
        'IP_ADDR': _IP_ADDR,
        'PORT': _PORT,
    }

    return render(request, 'record/view_bill.html', context)


@login_required
def each_bill(request, bill_id):
    """
    To view a specific Bill

    Args:
        request ([type]): [description]
        bill_id (int): id of bill
    """

    active_user = request.user
    bill = get_object_or_404(Bill, pk=bill_id)

    if active_user in bill.group.users.all():
        context = {
            "bill": bill,
            'profile_list': get_groups(active_user)
        }

        return render(request, 'record/each_bill.html', context)

    # else
    return redirect('home:group-error')


@login_required
def bill_delete(request, bill_id):
    """
    Delets a Bill and redirectes

    Args:
        request ([type]): [description]
        bill_id (int): id of bill
    """

    active_user = request.user
    bill = get_object_or_404(Bill, pk=bill_id)

    if active_user in bill.group.users.all():
        if request.method == 'POST':
            group_id = bill.group.pk
            bill.delete()

            return redirect('home:group', group_id)

    # else
    return redirect('home:group-error')


@login_required
def edit_bill(request, bill_id):
    """
    To edit a specific bill

    Args:
        request ([type]): [description]
        bill_id (int): id of bill
    """

    active_user = request.user
    bill = get_object_or_404(Bill, pk=bill_id)

    if active_user in bill.group.users.all():
        group_name = get_object_or_404(Group, pk=bill.group.pk)

        if request.method == "POST":
            form = BillForm(request.POST or None,
                            instance=bill, group_name=group_name)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('home:group', bill.group.pk)

        else:
            form = BillForm(request.POST or None,
                            instance=bill, group_name=group_name)

        context = {
            'form': form,
            'profile_list': get_groups(active_user)
        }

        return render(request, 'record/bill-edit.html', context)

    # else
    return redirect('home:group-error')


@login_required
def category_manage(request, group_id):
    """
    Page to Manage Categories.
    To delete Categories mainly

    Args:
        request ([type]): [description]
        group_id (int): id of group
    """

    active_user = request.user
    group = get_object_or_404(Group, id=group_id)

    if active_user in group.users.all():
        category_list = Category.objects.filter(group=group)

        context = {
            'category': category_list,
            'profile_list': get_groups(active_user)
        }

        return render(request, 'record/category_delete.html', context)

    # else
    return redirect('home:group-error')


@login_required
def category_delete(request, category_id):
    """
    Delete specified category

    Args:
        category_id (int): id of category
    """

    active_user = request.user
    category = get_object_or_404(Category, id=category_id)
    group_id = category.group.pk
    group = get_object_or_404(Group, id=group_id)

    if active_user in group.users.all():
        category.delete()

        return redirect('home:category-manage', group_id)

    # else
    return redirect('home:group-error')


@login_required
def group_management(request):
    """
    Management of Group.
    Deleting Group, Leaving a group and kicking someone from the group.
    """

    active_user = request.user
    users_of_groups = None
    groups = Group.objects.filter(users=active_user)

    for i in groups:
        if users_of_groups:
            users_of_groups |= i.users.all()
        else:
            users_of_groups = i.users.all()

    context = {
        'group_list': groups,
        'users': users_of_groups.distinct() if users_of_groups else None,
        'active_user': active_user,
        'profile_list': get_groups(active_user)
    }
    return render(request, 'record/view_management.html', context)


@login_required
def group_leave(request, group_id):
    """
    To leave a group

    Args:
        group_id (int): id of group
    """

    active_user = request.user
    group = get_object_or_404(Group, id=group_id)

    if active_user in group.users.all():
        group.users.remove(active_user)

        return redirect('home:group-manage')

    # else
    return redirect('home:group-error')


@login_required
def group_delete(request, group_id):
    """
    Delete the specified group if admin

    Args:
        group_id (int): id of group
    """

    active_user = request.user
    group = get_object_or_404(Group, id=group_id)

    if active_user == group.admin:
        group.delete()

        return redirect('home:group-manage')

    # else
    return redirect('home:group-error')


@login_required
def group_leave_user(request, group_id, user_id):
    active_user = request.user
    group = get_object_or_404(Group, id=group_id, admin=active_user)
    user = get_object_or_404(User, id=user_id)

    if active_user == group.admin:
        if user in group.users.all() and user != active_user:
            group.users.remove(user)
    else:
        return redirect('home:group-error')

    return redirect('home:group-manage')


@login_required
def group_new(request):
    active_user = request.user

    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            active_user = request.user
            post.admin = active_user
            post.save()
            post.users.add(active_user)
            post.save()
            messages.success(request, f"New Group Created!")
            return redirect('home:home')
    else:
        form = GroupForm()

    context = {
        'form': form,
        'profile_list': get_groups(active_user)
    }
    return render(request, 'registry/group.html', context)


@login_required
def group_join(request):
    active_user = request.user

    if request.method == "POST":
        form = JoinGroupForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            group_name = form.cleaned_data.get('name_group')
            group_password = form.cleaned_data.get('password_group')

            group = get_object_or_404(Group, name=group_name)

            if group.password == group_password:
                active_user = request.user
                group.users.add(active_user)
                try:
                    group.save()
                except IntegrityError:
                    messages.success(
                        request, f"You already belong to this group!")
                    return redirect('home:home')
                else:
                    messages.success(
                        request, f"Joined the Group {group_name}!")
                    return redirect('home:home')

            # else
            messages.warning(request, 'Group Name and Password not matching!!')
            return redirect('user:group-join')
    else:
        form = JoinGroupForm()

    context = {
        'form': form,
        'profile_list': get_groups(active_user)
    }

    return render(request, 'registry/profile.html', context)
