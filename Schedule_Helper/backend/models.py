from django.db import models
from django.utils.crypto import get_random_string


days_choice = (
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
)


def get_rand():
    return get_random_string(20)


class Groups(models.Model):
    gid = models.CharField(
        max_length=20,
        primary_key=True,
        default=get_rand,
        verbose_name='Group ID'
    )
    faculty = models.CharField(
        max_length=10,
        verbose_name='Faculty name'
    )
    gnum = models.SmallIntegerField(
        verbose_name='Group number'
    )

    week_reverse = models.BooleanField(
        verbose_name='Week reverse',
        default=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['faculty', 'gnum'],
                name='unique_group'
            )
        ]
        verbose_name = 'Group'

    def __str__(self):
        return f'{self.faculty}-{str(self.gnum)}'


class Profiles(models.Model):
    user_id = models.PositiveIntegerField(
        primary_key=True,
        verbose_name='User chat id'
    )
    username = models.CharField(
        max_length=32,
        null=True,
    )
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE
    )
    notification = models.BooleanField(
        default=True,
        verbose_name='Notifications for the user',
        null=True,
    )
    is_admin = models.BooleanField(
        default=False,
        null=True,
    )
    is_moderator = models.BooleanField(
        default=False,
        null=True,
    )

    class Meta:
        verbose_name = 'User profile'

    def __str__(self):
        return self.username if self.username else str(self.user_id)

    @property
    def deep_link(self):
        return f't.me/{self.username}' if self.username else None


class Schedule(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Pair name'
    )
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE
    )
    day = models.CharField(
        max_length=10,
        choices=days_choice,
        verbose_name='day'
    )
    number = models.SmallIntegerField(
        verbose_name='Pair number'
    )
    week_type = models.CharField(
        max_length=4,
        choices=(
            ('odd', 'Odd'),
            ('even', 'Even'),
        ),
        default='odd',
        verbose_name='Type of week'
    )
    start_time = models.CharField(
        verbose_name='Start pair',
        max_length=5,
        null=True,
        blank=True
    )
    end_time = models.CharField(
        verbose_name='End pair',
        max_length=5,
        null=True,
        blank=True
    )
    classroom = models.CharField(
        max_length=200,
        verbose_name='Classroom'
    )
    url = models.URLField(
        null=True,
        blank=True,
        verbose_name='URL'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group_id', 'day', 'number', 'week_type'],
                name='unique_sdl'),
        ]
        verbose_name = 'Schedule'
