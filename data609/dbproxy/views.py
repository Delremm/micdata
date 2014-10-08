from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

import random

from dbproxy.models import Profile, Node, NodeUser

from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)

        context['profile'] = random.randrange(1, 100)

        return context

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        return self.render_to_response(ctx)


class ManageView(LoginRequiredMixin, TemplateView):
    template_name = "manage.html"

    def get_context_data(self, **kwargs):
        context = super(ManageView, self).get_context_data(**kwargs)
        context['number'] = random.randrange(1, 100)

        return context

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data()
        ctx['nodes'] = Node.objects.filter(
            user=request.user, is_grafanadb=False)
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        if 'node_name' in request.POST:
            print('add node')

        ctx = self.get_context_data()
        return self.render_to_response(ctx)
