from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import Profiles, Schedule, Groups


def create_action(data):
    def action(modeladmin, request, queryset):
        for objects in queryset:
            objects.id = None
            objects.group_id = data['gid']
            objects.save()

    name = "mark_%s" % (data['gid'],)
    return [name, (action, name, "Dublicate and change group to %s" % (data['faculty'] + str(data['gnum']), ))]


@admin.action(description='OFF notif')
def off_notif(self, request, queryset):
    if queryset.update(notification=True):
        updated = queryset.update(notification=False)
        self.message_user(request, ngettext(
            '%d notification changed to OFF.',
            '%d notifications changed to OFF.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.action(description='ON notif')
def on_notif(self, request, queryset):
    if queryset.update(notification=False):
        updated = queryset.update(notification=True)
        self.message_user(request, ngettext(
            '%d notification changed to ON.',
            '%d notifications changed to ON.',
            updated,
        ) % updated, messages.SUCCESS)


@admin.register(Profiles)
class Profile_Admin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'group_id', 'notification', 'deep_link')
    list_filter = ("is_admin", "is_moderator")
    actions = [off_notif, on_notif]


@admin.register(Schedule)
class Schedule_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'day', 'number', 'week_type', 'classroom', 'start_time', 'end_time')
    list_display_links = ('name',)
    list_filter = ('group_id', 'week_type', 'day')

    def get_actions(self, request):
        actions = super(Schedule_Admin, self).get_actions(request)
        data = [action for action in Groups.objects.order_by().values('gid', 'faculty', 'gnum')]
        actions.update(dict(create_action(groups) for groups in data))
        return actions


@admin.register(Groups)
class Groups_Admin(admin.ModelAdmin):
    list_display = ('gid', 'faculty', 'gnum')
