from django.db import models
from django.utils import timezone

from extensions.utils import jalali_converter, get_filename_ext


def upload_to_Model_image(instance, filename):
    name, ext = get_filename_ext(filename)
    return f"panel/images/backgrounds/video/{instance.title}_{instance.pub_date}{ext}"
