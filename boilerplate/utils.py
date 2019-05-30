from django.contrib.admin.utils import NestedObjects
from django.db import router
from django.utils.html import format_html
from django.utils.text import capfirst


def get_deleted_objects(objs, request):
    try:
        obj = objs[0]
    except IndexError:
        return [], {}, set(), []
    else:
        using = router.db_for_write(obj._meta.model)
    collector = NestedObjects(using=using)
    collector.collect(objs)
    perms_needed = set()

    def format_callback(obj):
        opts = obj._meta
        no_edit_link = '%s: %s' % (capfirst(opts.verbose_name), obj)
        perms_needed.add(opts.verbose_name)

        try:
            return format_html('{}: <a href="{}">{}</a>',
                               capfirst(opts.verbose_name),
                               obj.get_absolute_url(),
                               obj)
        except AttributeError:
            return no_edit_link

    to_delete = collector.nested(format_callback)

    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {model._meta.verbose_name_plural: len(
        objs) for model, objs in collector.model_objs.items()}

    return to_delete, model_count, perms_needed, protected
