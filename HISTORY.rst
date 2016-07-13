.. :changelog:

History
-------
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