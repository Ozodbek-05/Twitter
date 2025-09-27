from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView
from accounts.forms import RegisterModelForm, LoginForm


class RegisterCreateView(CreateView):
    model = User
    template_name = 'login.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        messages.success(request=self.request, message="Successfully registered")
        return super().form_valid(form)

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for error in value:
                messages.error(request=self.request, message=error)
        return super().form_invalid(form)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('pages:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        if user:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('pages:home')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Logged out successfully")
        return redirect(self.url)
