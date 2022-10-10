from wagtail.admin.panels import Panel


class CustomPanel(Panel):
    """
    Example how to render a custom template as a panel in admin.

    In the template context, you will have `self.instance` as
    the instance of your object.
    """

    class BoundPanel(Panel.BoundPanel):
        template_name = "example/custom_panel.html"
