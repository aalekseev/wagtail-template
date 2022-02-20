"""
Wagtail default dashboard overwrites.

See https://docs.wagtail.org/en/stable/reference/hooks.html#admin-modules
"""
from django.utils.safestring import mark_safe

from wagtail.admin.ui.components import Component
from wagtail.core import hooks

class WelcomePanel(Component):
    order = 50

    def render_html(self, parent_context):
        return mark_safe("""
        <section class="panel summary nice-padding">
          <h3>No, but seriously -- welcome to the admin homepage.</h3>
        </section>
        """)


@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(WelcomePanel())
