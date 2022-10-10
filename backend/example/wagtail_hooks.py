from django.urls import path, reverse

from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)
from wagtail.core import hooks

from example.models import Category, Item, Meeting
from example.views import index
from generic.admin import RestrictedModelAdmin


# ----
# Example how to add custom button to the list view in admin
# ----
class CustomButtonHelper(ButtonHelper):
    """
    This class allows adding customized buttons to the listing admin view.
    """

    # Define classes for our button, here we can set an icon, for example
    view_button_classnames = ["button-small", "icon", "icon-upload"]

    def import_button(self, obj):  # pylint: disable=unused-argument
        """Define a label for our button."""

        return {
            # In real-life scenario will be reverse to admin page
            "url": "https://google.com",
            "label": "Import Attendants",
            "classname": self.finalise_classname(self.view_button_classnames),
            "title": "Import Attendants",
        }

    def get_buttons_for_obj(
        self, obj, exclude=None, classnames_add=None, classnames_exclude=None
    ):
        """
        This function is used to gather all available buttons.
        We append our custom button to the buttons list.
        """
        buttons = super().get_buttons_for_obj(
            obj, exclude, classnames_add, classnames_exclude
        )
        if "view" not in (exclude or []):
            buttons.append(self.import_button(obj))
        return buttons


# And this is how it is added to the modeladmin class
class MeetingAdmin(ModelAdmin):
    model = Meeting
    menu_label = "Meetings"
    menu_icon = "date"
    search_fields = ("title",)
    list_display = ("title", "record_date")
    list_filter = ("record_date",)
    date_hierarchy = "record_date"
    button_helper_class = CustomButtonHelper
    list_export = ("title", "record_date")


modeladmin_register(MeetingAdmin)


# ----
# Example how to add custom menu item that will show custom admin url.
# ----
@hooks.register("register_admin_urls")
def register_calendar_url():
    return [
        path("calendar/", index, name="calendar"),
    ]


@hooks.register("register_admin_menu_item")
def register_calendar_menu_item():
    return MenuItem("Calendar", reverse("calendar"), icon_name="date")


# ----
# Example how to create a custom menu item with sub-items
# ----
class CategoryAdmin(RestrictedModelAdmin):
    model = Category
    menu_label = "Categories"
    menu_icon = "placeholder"
    search_fields = ("name",)


class ItemAdmin(RestrictedModelAdmin):
    model = Item
    menu_label = "Items"
    menu_icon = "tag"
    search_fields = ("name",)


class InventoryAdminGroup(ModelAdminGroup):
    menu_label = "Inventory"
    menu_icon = "folder-open-inverse"
    items = (CategoryAdmin, ItemAdmin)


modeladmin_register(InventoryAdminGroup)
