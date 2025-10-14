from django.contrib.auth.hashers import make_password

from account.models import Ticket
from cart.models import Cart, UserPlan
from django.contrib.auth import get_user_model

User = get_user_model()


class FieldsMixinCart():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.queryset = Cart.objects.filter()
        else:
            self.queryset = Cart.objects.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class FieldsMixinPlan():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.queryset = UserPlan.objects.filter()
        else:
            self.queryset = UserPlan.objects.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)


class FieldsCustomUserListMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.queryset = User.objects.filter()
        else:
            pk = request.user.pk
            self.queryset = User.objects.filter(pk=pk)
        return super().dispatch(request, *args, **kwargs)


class ValidFormMixin():
    def get_initial(self):
        initial = super(ValidFormMixin, self).get_initial()
        global password_unChange
        password_unChange = self.object.password  # hash password
        initial["password"] = self.object.pass_per_save  # 1234
        return initial

    def form_valid(self, form):
        cleend_form = form
        password = cleend_form.cleaned_data.get("password")
        pass_per_save = cleend_form.cleaned_data.get("pass_per_save")
        self.user = form.save(commit=False)
        if password != pass_per_save:
            self.user.pass_per_save = password
            self.user.password = make_password(password)
        else:
            self.user.password = password_unChange
        self.user.save()
        return super(ValidFormMixin, self).form_valid(form)


class FieldsMixinTicket():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.queryset = Ticket.objects.filter()
        else:
            self.queryset = Ticket.objects.filter(user=request.user)
        return super().dispatch(request, *args, **kwargs)
