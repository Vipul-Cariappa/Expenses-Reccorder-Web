from itertools import chain
from django import forms
from .models import Category, Bill, Group


class BillForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = ('name', 'date', 'category', 'amount', 'discription')

    def __init__(self, *args, **kwargs):
        group_name = kwargs.pop('group_name', None)
        super(BillForm, self).__init__(*args, **kwargs)

        x = Category.objects.filter(group=group_name)
        self.fields['category'].queryset = x


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'password')


class JoinGroupForm(forms.ModelForm):
    name_group = forms.CharField(max_length=100)
    password_group = forms.CharField(
        max_length=30, widget=forms.PasswordInput())

    class Meta:
        model = Group
        fields = ('name_group', 'password_group')
