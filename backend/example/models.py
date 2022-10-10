from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    TabbedInterface,
)

from example.panels import CustomPanel
from generic.models import BaseModel


class Category(BaseModel):
    # See https://github.com/typeddjango/django-stubs/issues/908
    name = models.CharField(max_length=255)  # type: ignore

    info_panels = [MultiFieldPanel([FieldPanel("name")])]
    edit_handler = TabbedInterface([ObjectList(info_panels, heading="Info")])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"


class Item(BaseModel):
    # See https://github.com/typeddjango/django-stubs/issues/908
    name = models.CharField(max_length=255)  # type: ignore
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # type: ignore
    article = models.CharField(max_length=255, null=True, blank=True)  # type: ignore

    info_panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("category"),
                FieldPanel("article"),
            ]
        )
    ]

    edit_handler = TabbedInterface([ObjectList(info_panels, heading="Info")])

    def __str__(self):
        return f"{self.category}/{self.name}"

    class Meta:
        unique_together = ("name", "category")
        ordering = ("category", "name")


class Meeting(BaseModel, ClusterableModel):
    # See https://github.com/typeddjango/django-stubs/issues/908
    title = models.CharField(max_length=255)  # type: ignore
    description = models.TextField(
        blank=True, help_text="Optional notes about the meeting"
    )  # type: ignore
    record_date = models.DateField(
        help_text="Set at which date the meeting is happening"
    )  # type: ignore

    info_panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("description"),
                FieldPanel("record_date"),
            ]
        )
    ]

    agenda_panels = [
        InlinePanel(
            "meeting_agenda_points",
            panels=[
                FieldPanel("title"),
                FieldPanel("description"),
                FieldRowPanel(
                    [
                        FieldPanel("start_time"),
                        FieldPanel("end_time"),
                    ]
                ),
            ],
        )
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(info_panels, heading="General Info"),
            ObjectList(agenda_panels, heading="Agenda Points"),
            CustomPanel(heading="Custom Panel"),
        ]
    )

    def __str__(self):
        return self.title
