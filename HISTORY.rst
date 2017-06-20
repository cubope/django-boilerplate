.. :changelog:

History
-------
0.5.8 (2017-06-19)
++++++++++++++++++
* Add: Send email without template, only with content

0.5.6 (2017-04-25)
++++++++++++++++++
* Fix: Django 1.11 compatibility

0.5.4 (2017-03-31)
++++++++++++++++++
* Add: `ModelImageThumbs` Python 3 support.
* Add: `six` requirements.txt

0.5.0 (2017-03-28)
++++++++++++++++++
* Add: `ExtraFormsAndFormsetsMixin` trasactions ar atomic now, if something fails nothings gets saved.

0.4.9 (2017-03-27)
++++++++++++++++++
* Fix: `ExtraFormsAndFormsetsMixin` parent response prevail.

0.4.8 (2017-03-27)
++++++++++++++++++
* Rename: `permissions.py` to `signals.py`
* Add: Documentation `add_view_permissions`
* Add: More tests

0.4.5 (2017-03-25)
++++++++++++++++++
* Remove: `templates` folder, `forms.py` and `views.py` no longer required,  no longer required, Django cover this.
* Add: Initial tests
* Update: PEP8
* Bug: `add_view_permissions` Python3 compatibility
* Add: Allow email testing
* Enhancement: Rename variables `formsets` to `formset_list` and `extra_forms` to `extra_form_list`

0.3.6 (2016-11-26)
++++++++++++++++++
* Fix: LoginForm username and password required fields

0.3.6 (2016-11-9)
++++++++++++++++++
* Fix: If doesn't found model name get form name

0.3.5 (2016-09-30)
++++++++++++++++++
* Fix: Raise PermissionDenied on NoLoginRequiredMixin

0.3.4 (2016-09-30)
++++++++++++++++++
* Fix: ModelImageThumb super class

0.3.3 (2016-08-30)
++++++++++++++++++
* Bug: Fix minor bugs

0.3.2 (2016-08-30)
++++++++++++++++++
* Add: Parent model mixins

0.3.0 (2016-08-29)
++++++++++++++++++
* Change: Improove mail, now it's a class not a function

0.2.8 (2016-08-19)
++++++++++++++++++
* Add: New model child action template tag

0.2.7 (2016-07-21)
++++++++++++++++++
* Fix: Mixin CreateModelMixin
* Improvement: No loger convert template tags to titles

0.2.5 (2016-06-26)
++++++++++++++++++
* Fix: PIL as new requirement
* Fix: Requirements
* Fix: Python3 compatibility

0.2.3 (2016-06-26)
++++++++++++++++++
* Added: `add_view_permissions`: Create a post migrate signal to add a new view
permission to all the model
* Added: `ModelImageThumbs`, and automatically create thumbnails from the images that you upload.

0.2.1 (2016-06-20)
++++++++++++++++++
* Fix: Forgot to import translation at `views.py`.

0.2.0 (2016-06-18)
++++++++++++++++++
* Rename: `views.py` to `mixins.py` because is the propper name
* Add: `boilerplate.py` with the default settings, you can customize your error messages.
* Add: `forms.py` Forms with validation to the following Views:
* Add: `views.py`: `LoginView`
* Add: `views.py`: `RecoverAccountView`
* Add: `views.py`: `RegistrationView`
* Add: `views.py`: `LoginView`

0.1.3 (2016-06-16)
++++++++++++++++++
* Fix: CRUD Messages Mixin conflict with Extra Forms and Formsets Mixin
* Fix: ExtraFormsandFormsetsMixin validate if `formset_list` or `extra_form_list` exists
* Fix: App template tags, didn't got the model information intead of the app information


0.1.0 (2016-06-12)
++++++++++++++++++
* Fix: CRUD Messages Mixin
* Bug: Variables got reasigned ExtraFormsAndFormsetsMixin on the get_context_data
* Convert spaces to tabs

0.0.1 (2016-06-6)
++++++++++++++++++
* project added
