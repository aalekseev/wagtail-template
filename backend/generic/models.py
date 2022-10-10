from django.contrib.auth import get_user_model
from django.db import models

from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class OwnersMixin(models.Model):
    owners = models.ManyToManyField(get_user_model(), null=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """
    Base model for this project.
    It has these fields:
    - id (which is unique UUID)
    - created
    - modified
    - is_removed (also has a manager which hides deleted objects)
    """

    class Meta:
        abstract = True
