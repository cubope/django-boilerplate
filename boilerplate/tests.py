# -*- coding: utf-8 -*-
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django import forms
from django.core.management import call_command
from django.contrib.messages import get_messages
from django.contrib.messages.storage import default_storage
from django.core.exceptions import PermissionDenied
from django.db.models import signals
from django.forms import inlineformset_factory
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import (
    AnonymousUser, ContentType, Permission, User
)
from django.test import RequestFactory, TestCase
try:
    from django.template import engines
except ImportError:
    from django.template.engines import Engine
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .mail import SendEmail
from .mixins import (
    NoLoginRequiredMixin, ActionListMixin, UserCreateMixin, CreateMessageMixin,
    UpdateMessageMixin, DeleteMessageMixin, ExtraFormsAndFormsetsMixin,
    ParentCreateMixin, ParentSingleObjectMixin
)
from .signals import add_view_permissions


class TestModelForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = User


class TestForm(forms.Form):
    name = forms.CharField()


TestFormSet = inlineformset_factory(
    ContentType,
    Permission,
    fields='__all__',
    min_num=0
)


def render_template(text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    try:
        template = engines['django'].from_string(text)
    except Exception:
        template = Engine().from_string(text)
    if not context:
        context = {}
    return template.render(context)


def render_template_with_boilerplate(text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    if not context:
        context = {}
    return render_template("{% load boilerplate %}" + text, context)


def render_template_with_form(text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    if not context:
        context = {}
    if 'form' not in context:
        context['form'] = TestForm()
    return render_template_with_boilerplate(text, context)


def render_template_with_form_model(text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    if not context:
        context = {}
    if 'form' not in context:
        context['form'] = TestModelForm()
    return render_template_with_boilerplate(text, context)


def render_template_with_formset(text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    if not context:
        context = {}
    if 'form' not in context:
        context['formset'] = TestFormSet()
    return render_template_with_boilerplate(text, context)


def render_template_with_object(obj, text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    if not context:
        context = {}
    if 'object' not in context:
        context['object'] = obj
    return render_template_with_boilerplate(text, context)


def render_template_with_object_list(object_list, text, context=None):
    """
    Create a template ``text`` that first loads boilerplate.
    """
    if not context:
        context = {}
    if 'object_list' not in context:
        context['object_list'] = object_list
    return render_template_with_boilerplate(text, context)


class TemplateTest(TestCase):
    def setUp(self):
        self.form_model = TestModelForm()
        self.form = TestForm()
        self.o_user = User.objects.create(
            username="test",
            email="test@test.com"
        )
        self.qs_user = User.objects.all()

    def test_form_model_name(self):
        res = render_template_with_form_model(
            '{{ form|form_model_name }}'
        )
        self.assertEqual('user', res)

        res = render_template_with_form(
            '{{ form|form_model_name }}'
        )
        self.assertEqual('TestForm', res)

    def test_form_model_name_plural(self):
        res = render_template_with_form_model(
            '{{ form|form_model_name_plural }}'
        )
        self.assertEqual('users', res)

    def test_form_model_url(self):
        res = render_template_with_form_model(
            '{{ form|form_model_url }}'
        )
        self.assertEqual('auth:user_list', res)

    def test_form_app_name(self):
        res = render_template_with_form_model(
            '{{ form|form_app_name }}'
        )
        self.assertEqual('Authentication and Authorization', res)

    def test_form_app_url(self):
        res = render_template_with_form_model(
            '{{ form|form_app_url }}'
        )
        self.assertEqual('auth:home', res)

    def test_form_prefix(self):
        res = render_template_with_form_model(
            '{{ form|form_prefix }}'
        )
        self.assertEqual('testmodelform', res)

    def test_formset_model_name(self):
        res = render_template_with_formset(
            '{{ formset|formset_model_name }}'
        )
        self.assertEqual('permission', res)

    def test_formset_model_name_plural(self):
        res = render_template_with_formset(
            '{{ formset|formset_model_name_plural }}'
        )
        self.assertEqual('permissions', res)

    def test_model_name(self):
        res = render_template_with_object(
            self.o_user,
            '{{ object|model_name }}'
        )
        self.assertEqual('user', res)

    def test_model_name_plural(self):
        res = render_template_with_object(
            self.o_user,
            '{{ object|model_name_plural }}'
        )
        self.assertEqual('users', res)

    def test_model_app_name(self):
        res = render_template_with_object(
            self.o_user,
            '{{ object|model_app_name }}'
        )
        self.assertEqual('Authentication and Authorization', res)

    def test_model_app_url(self):
        res = render_template_with_object(
            self.o_user,
            '{{ object|model_app_url }}'
        )
        self.assertEqual('auth:home', res)

    def test_model_url(self):
        res = render_template_with_object(
            self.o_user,
            '{{ object|model_url }}'
        )
        self.assertEqual('auth:user_list', res)

    def test_queryset_app_name(self):
        res = render_template_with_object_list(
            self.qs_user,
            '{{ object_list|queryset_app_name }}'
        )
        self.assertEqual('Authentication and Authorization', res)

    def test_queryset_app_url(self):
        res = render_template_with_object_list(
            self.qs_user,
            '{{ object_list|queryset_app_url }}'
        )
        self.assertEqual('auth:home', res)

    def test_queryset_model_name_plural(self):
        res = render_template_with_object_list(
            self.qs_user,
            '{{ object_list|queryset_model_name_plural }}'
        )
        self.assertEqual('users', res)

    def test_queryset_model_url(self):
        res = render_template_with_object_list(
            self.qs_user,
            '{{ object_list|queryset_model_url }}'
        )
        self.assertEqual('auth:user_list', res)


class SignalTest(TestCase):
    def test_migration_output(self):
        signals.post_migrate.connect(add_view_permissions)
        out = StringIO()
        call_command('migrate', stdout=out)
        # self.assertIn('Added view permission', out.getvalue())


class NoLoginRequiredView(NoLoginRequiredMixin, TemplateView):
    template_name = 'any_template.html'


class ActionListView(ActionListMixin, TemplateView):
    action_list = (
        'Add', 'Change', 'Delete'
    )
    template_name = 'any_template.html'


class UserCreateView(UserCreateMixin, CreateView):
    fields = (
        'content_type', 'object_id', 'object_repr', 'action_flag',
    )
    model = LogEntry
    success_url = '/fake-path-success'

    def form_valid(self, form):
        super(UserCreateView, self).form_valid(form)
        return self.object


class CreateMessageView(CreateMessageMixin, CreateView):
    fields = ('username', 'email')
    model = User
    success_url = '/fake-path-success'

    def form_valid(self, form):
        super(CreateMessageView, self).form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class UpdateMessageView(UpdateMessageMixin, UpdateView):
    fields = ('username', 'email')
    model = User
    success_url = '/fake-path-success'

    def get_object(self):
        obj, created = User.objects.get_or_create(username="gclooney")
        return obj

    def form_valid(self, form):
        super(UpdateMessageView, self).form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class DeleteMessageView(DeleteMessageMixin, DeleteView):
    model = User
    success_url = '/fake-path-success'

    def get_object(self):
        obj, created = User.objects.get_or_create(username="gclooney")
        return obj

    def delete(self, request, *args, **kwargs):
        super(DeleteMessageView, self).delete(request, *args, **kwargs)
        return self.render_to_response({})


class ParentCreateView(ParentCreateMixin, CreateView):
    fields = ('codename', 'name')
    model = Permission
    parent_model = ContentType
    parent_relation_field = 'content_type'
    success_url = '/fake-path-success'

    def form_valid(self, form):
        super(ParentCreateView, self).form_valid(form)
        return self.object


class ParentSingleObjectView(ParentSingleObjectMixin, DetailView):
    model = Permission
    parent_model = ContentType
    parent_relation_field = 'content_type'


class ExtraFormsAndFormsetsView(ExtraFormsAndFormsetsMixin, UpdateView):
    PermissionFormSet = inlineformset_factory(
        ContentType,
        Permission,
        fields='__all__',
        extra=1,
        can_delete=False,

    )
    fields = '__all__'
    model = ContentType
    formset_list = (
        PermissionFormSet,
    )
    success_url = '/fake-path-success'

    def form_valid(self, form, extra_forms=None, formsets=None):
        super(ExtraFormsAndFormsetsView, self).form_valid(
            form, extra_forms, formsets
        )
        return self.object


class ExtraFormsAndFormsetsAndUpdateView(
    ExtraFormsAndFormsetsMixin, UpdateMessageMixin, UpdateView
):
    PermissionFormSet = inlineformset_factory(
        ContentType,
        Permission,
        fields='__all__',
        extra=1,
        can_delete=False,

    )
    fields = '__all__'
    model = ContentType
    formset_list = (
        PermissionFormSet,
    )
    success_url = '/fake-path-success'

    def form_valid(self, form, extra_forms=None, formsets=None):
        super(ExtraFormsAndFormsetsAndUpdateView, self).form_valid(
            form, extra_forms, formsets
        )
        return self.object


class MixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com'
        )

    def test_no_login_required_mixin_anonymous_user(self):
        request = self.factory.get('/fake-path')
        request.user = AnonymousUser()

        response = NoLoginRequiredView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_no_login_required_mixin_user(self):
        request = self.factory.get('/fake-path')
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            NoLoginRequiredView.as_view()(request)

    def test_action_list_mixin(self):
        request = self.factory.get('/fake-path')
        response = ActionListView.as_view()(request)
        self.assertEqual(
            response.context_data['action_list'],
            ActionListView.action_list
        )

    def test_user_create_mixin(self):
        content_type = ContentType.objects.get(
            app_label="auth", model="user"
        )

        request = self.factory.post('/fake-path', {
            'content_type': content_type.id,
            'object_id': self.user.id,
            'object_repr': "Test {}".format(self.user),
            'action_flag': 1,
            'change_message': '',
        })
        request.user = self.user
        response = UserCreateView.as_view()(request)
        self.assertEqual(isinstance(response, LogEntry), True)
        self.assertNotEqual(response, None)

    def test_create_message_mixin(self):
        request = self.factory.post('/fake-path', {
            'username': 'gclooney',
            'email': 'gclooney@test.com',
        })
        request._messages = default_storage(request)
        CreateMessageView.as_view()(request)

        self.assertEqual(len(get_messages(request)), 1)

    def test_update_message_mixin(self):
        request = self.factory.post('/fake-path', {
            'username': 'gclooney',
            'email': 'gclooney@test.com',
        })
        request._messages = default_storage(request)
        UpdateMessageView.as_view()(request)

        self.assertEqual(len(get_messages(request)), 1)

    def test_delete_message_mixin(self):
        request = self.factory.post('/fake-path', {})
        request._messages = default_storage(request)
        DeleteMessageView.as_view()(request)

        self.assertEqual(len(get_messages(request)), 1)

    def test_parent_create_mixin(self):
        content_type = ContentType.objects.get(
            app_label='contenttypes', model='contenttype',
        )

        request = self.factory.post('/fake-path', {
            'codename': 'test_user',
            'name': 'Test user'
        })
        response = ParentCreateView.as_view()(
            request,
            pk_parent=content_type.id,
        )
        self.assertEqual(response.content_type, content_type)

    def test_parent_single_object_mixin(self):
        content_type = ContentType.objects.get(
            app_label='contenttypes', model='contenttype',
        )
        permission, created = Permission.objects.get_or_create(
            content_type=content_type,
            codename='test_user',
            name='Test user'
        )

        request = self.factory.get('/fake-path')
        response = ParentSingleObjectView.as_view()(
            request,
            pk_parent=content_type.id,
            pk=permission.id
        )
        self.assertEqual(response.context_data['object'], permission)

    def test_extra_forms_and_formsets_mixin(self):
        content_type = ContentType.objects.get(
            app_label='contenttypes', model='contenttype',
        )

        request = self.factory.get('/fake-path')
        response = ExtraFormsAndFormsetsView.as_view()(
            request,
            pk=content_type.pk,
        )
        self.assertNotEqual(response.context_data['form'], None)
        self.assertEqual(len(response.context_data['formset_list']), 1)

        request = self.factory.post('/fake-path', {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'permission_set-TOTAL_FORMS': 4,
            'permission_set-INITIAL_FORMS': 3,
            'permission_set-MIN_NUM_FORMS': 0,
            'permission_set-MAX_NUM_FORMS': 1000,
            'permission_set-0-name': "Can add content type",
            'permission_set-0-codename': "add_contenttype",
            'permission_set-0-id': 13,
            'permission_set-0-content_type': 5,
            'permission_set-1-name': "Can change content type",
            'permission_set-1-codename': "change_contenttype",
            'permission_set-1-id': 14,
            'permission_set-1-content_type': 5,
            'permission_set-2-name': "Can delete content type",
            'permission_set-2-codename': "delete_contenttype",
            'permission_set-2-id': 15,
            'permission_set-2-content_type': 5,
            'permission_set-3-name': "Can test content type",
            'permission_set-3-codename': "test_contenttype",
            'permission_set-3-content_type': 5,
        })
        response = ExtraFormsAndFormsetsView.as_view()(
            request,
            pk=content_type.pk,
        )
        self.assertEqual(
            response.permission_set.get(codename='test_contenttype').codename,
            'test_contenttype'
        )

    def test_extra_forms_and_formsets_and_update_message_mixin(self):
        content_type = ContentType.objects.get(
            app_label='contenttypes', model='contenttype',
        )

        request = self.factory.post('/fake-path', {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'permission_set-TOTAL_FORMS': 4,
            'permission_set-INITIAL_FORMS': 3,
            'permission_set-MIN_NUM_FORMS': 0,
            'permission_set-MAX_NUM_FORMS': 1000,
            'permission_set-0-name': "Can add content type",
            'permission_set-0-codename': "add_contenttype",
            'permission_set-0-id': 13,
            'permission_set-0-content_type': 5,
            'permission_set-1-name': "Can change content type",
            'permission_set-1-codename': "change_contenttype",
            'permission_set-1-id': 14,
            'permission_set-1-content_type': 5,
            'permission_set-2-name': "Can delete content type",
            'permission_set-2-codename': "delete_contenttype",
            'permission_set-2-id': 15,
            'permission_set-2-content_type': 5,
            'permission_set-3-name': "Can test content type",
            'permission_set-3-codename': "test_contenttype",
            'permission_set-3-content_type': 5,
        })
        request._messages = default_storage(request)
        response = ExtraFormsAndFormsetsAndUpdateView.as_view()(
            request,
            pk=content_type.pk,
        )
        self.assertEqual(
            response.permission_set.get(codename='test_contenttype').codename,
            'test_contenttype'
        )
        self.assertEqual(len(get_messages(request)), 1)


class MailTest(TestCase):
    def test_send_email_error(self):
        email = SendEmail(
            to='test@test.com',
            subject="This email should raise an error"
        )
        with self.assertRaises(Exception):
            email.send()

    def test_send_email_only_content(self):
        email = SendEmail(
            to='test@test.com',
            subject="This is the subject",
            content="This is the email content."
        )
        self.assertEqual(email.send(), 1)
