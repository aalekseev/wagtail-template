from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = (
    [
        path("admin/", include(wagtailadmin_urls)),
        # Login, logout and reset password views
        # See in templates folder "registration" for overwritten templates
        path("accounts/", include("django.contrib.auth.urls")),
        path("hijack/", include("hijack.urls")),
        path("docs/", include(wagtaildocs_urls)),
        path("", include(wagtail_urls)),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
