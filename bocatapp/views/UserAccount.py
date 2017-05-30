from django.db import transaction
from django.views.generic import detail, edit
from django.shortcuts import render
from bocatapp.forms import UserForm, PasswordForm
from django.utils.translation import ugettext_lazy as _


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
        context = {
            'type': _('Edit profile'),
            'user_form': user_form
        }
        return render(request, '../templates/forms/user_edit.html', context)

    @transaction.atomic
    def post(self, request):
        if request.user.is_authenticated():
            user_form = UserForm(data=request.POST, instance=request.user, prefix='user')
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.save()
                return render(request, '../templates/myaccount.html')
            else:
                message = ""
                for field, errors in (user_form.errors.items()):
                    for error in errors:
                        message += error
                context = {
                    'user_form': user_form,
                    'message': message
                }
                return render(request, '../templates/forms/user_edit.html', context)
        else:
            return render(request, '../templates/forbidden.html')


class PasswordEdit(edit.BaseUpdateView):
    def get(self, request):
        if request.user.is_authenticated():
            password_form = PasswordForm()
            context = {
                'password_form': password_form
            }
            return render(request, '../templates/forms/password_edit.html', context)

    @transaction.atomic
    def post(self, request):
        user = request.user
        if user.is_authenticated():
            password_form = PasswordForm(request.POST, user=user)
            if password_form.is_valid():
                password = password_form.cleaned_data.get('password')
                user.set_password(password)
                user.save()
                return render(request, '../templates/myaccount.html')
            else:
                message = []
                for error in password_form.errors['__all__']:
                    message.append(error)
                context = {
                    'password_form': password_form,
                    'error_messages': message
                }
                return render(request, '../templates/forms/password_edit.html', context)
        else:
            return render(request, '../templates/forbidden.html')
