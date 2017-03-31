# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

from PIL import Image
import six


class ModelImageThumbs(object):
    IMAGESIZES = None

    def save(self, *args, **kwargs):
        response = super(ModelImageThumbs, self).save(*args, **kwargs)

        if self.image:
            filename = str(self.image.name)
            imgFile = Image.open(storage.open(filename))

            if imgFile.mode not in ('L', 'RGB'):
                imgFile = imgFile.convert('RGB')

            for field_name, size in six.iteritems(self.IMAGESIZES):
                field = getattr(self, field_name)

                if not field:
                    working = imgFile.copy()
                    working = working.resize(size, Image.ANTIALIAS)
                    fp = StringIO()
                    working.save(fp, 'JPEG', quality=95)
                    cf = ContentFile(fp.getvalue())
                    field.save(name=self.image.name, content=cf, save=True)
        else:
            for field_name, size in six.iteritems(self.IMAGESIZES):
                field = getattr(self, field_name)
                field.delete(save=True)

        return response
