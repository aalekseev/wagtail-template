from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.contrib.modeladmin.views import CreateView, IndexView


class SuperuserOnlyPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return user.is_superuser

    def user_can_create(self, user):
        return user.is_superuser

    def user_can_edit_obj(self, user, obj):
        return user.is_superuser

    def user_can_delete_obj(self, user, obj):
        return user.is_superuser


class RestrictedPermissionHelper(PermissionHelper):
    def user_can_list(self, user):
        return True

    def user_can_create(self, user):
        return True

    def user_can_edit_obj(self, user, obj):
        return obj.owners.filter(pk=user.pk).exists()

    def user_can_delete_obj(self, user, obj):
        return obj.owners.filter(pk=user.pk).exists()


class CanOnlyListPermissionHelper(RestrictedPermissionHelper):
    def user_can_create(self, user):
        return False


class RestrictedCreateView(CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        instance = self.get_instance()
        instance.owners.filter(pk=self.request.user.pk).exists()
        instance.save()
        return response


class RestrictedIndexView(IndexView):
    def get_base_queryset(self, request=None):
        request = request or self.request
        return super().get_base_queryset(request).filter(owners=request.user)


class SuperuserOnlyModelAdmin(ModelAdmin):
    permission_helper_class = SuperuserOnlyPermissionHelper


class RestrictedModelAdmin(ModelAdmin):
    index_view_class = RestrictedIndexView
    create_view_class = RestrictedCreateView
    permission_helper_class = RestrictedPermissionHelper
    # Disable history view as it leaks information
    # about other users actions
    history_view_enabled = False
