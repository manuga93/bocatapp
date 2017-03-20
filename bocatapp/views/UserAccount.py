from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import detail, edit
from django.shortcuts import render, get_object_or_404
from bocatapp.forms import UserForm, UserProfileForm


class UserAccountView(detail.DetailView):
    def get(self, request):
        if request.user.is_authenticated():
            context = {'user': request.user}
            return render(request, '../templates/myaccount.html', context)
        else:
            return render(request, '../templates/forbidden.html')


class UserEdit(edit.BaseUpdateView):
    def get(self, request):
        user_form = UserForm(instance=request.user, prefix='user')
        profile_form = UserProfileForm(instance=request.user.profile, prefix='profile')
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, '../templates/forms/user_edit.html', context)

    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated():
            form = UserForm(data=request.POST, instance=request.user, prefix='user')
            profile_form = UserProfileForm(data=request.POST, instance=request.user.profile, prefix='profile')
            if form.is_valid() and profile_form.is_valid():
                user = form.save(commit=False)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                context = {'user': request.user}
                return render(request, '../templates/myaccount.html', context)
            else:
                message = ""
                for field, errors in form.errors.items():
                    for error in errors:
                        message += error
                context = {
                    'form': form, 'message': message
                }
                return render(request, '../templates/forms/user_edit.html', context)
        else:
            return render(request, '../templates/forbidden.html')
