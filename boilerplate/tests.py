from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import (ContentType, Permission, User)
from django.test import TestCase
from django.template import engines


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
    template = engines['django'].from_string(text)
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
