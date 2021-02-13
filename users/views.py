from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView
from .forms import SignUpForm, UserProfileForm
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.mixins import AccessMixin

User = get_user_model()


# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('activation')
    template_name = "user/register.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return render(self.request, "user/register.html", {"form": self.get_form()})

    def form_valid(self, form):
        form = form.save(commit=False)
        form.is_active = False
        form.save()
        current_site = get_current_site(self.request)
        subject = "Activate your account"
        message = render_to_string("user/activation.html", {
            "form": form,
            "domain": current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(form.pk)),
            'token': account_activation_token.make_token(form),
        })
        form.email_user(subject=subject, message=message)
        return HttpResponse('ثبت نام با موفقیت انجام پذیرفت. لینک فعالسازی به ایمیلتان ارسال گردید.')

    def form_invalid(self, form):
        return super().form_invalid(form)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('register')
    else:
        return render(request, 'user/activation_invalid.html')


class Login(LoginView):

    template_name = "user/login.html"
    redirect_field_name = "home"


class ProfileView(LoginRequiredMixin, AccessMixin, DetailView):
    template_name = 'user/profile.html'
    model = User
    permission_denied_message = "اجازه دسترسی به این صفحه را ندارید."
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        print(request.user.id)
        if int(request.user.id) != int(self.kwargs['pk']):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class EditUserProfileView(LoginRequiredMixin, AccessMixin, UpdateView):
    template_name = "user/edit_profile.html"
    model = User
    form_class = UserProfileForm
    permission_denied_message = "اجازه دسترسی به این صفحه را ندارید."
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        print(request.user.id)
        if int(request.user.id) != int(self.kwargs['pk']):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse("profile", kwargs={'pk': self.kwargs['pk']})


