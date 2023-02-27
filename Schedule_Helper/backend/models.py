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

start_time_choice = (
    ('09:00', '09:00 |1| 2-3курс'),
    ('10:50', '10:50 |2| 2-3курс'),
    ('12:40', '12:40 |3| 2-3курс'),
    ('14:10', '14:10 |4| 2-3курс'),
    ('15:40', '15:40 |5| 2-3курс'),
    ('17:10', '17:10 |6| 2-3курс'),

    ('09:30', '09:30 |1| 1-4курс'),
    ('11:20', '11:20 |2| 1-4курс'),
    ('13:10', '13:10 |3| 1-4курс'),
    ('14:40', '14:40 |4| 1-4курс'),
    ('16:10', '16:10 |5| 1-4курс'),
    ('17:40', '17:40 |6| 1-4курс'),
)

end_time_choice = (
    ('10:20', '10:20 |1| 2-3курс'),
    ('12:10', '12:10 |2| 2-3курс'),
    ('14:00', '14:00 |3| 2-3курс'),
    ('15:30', '15:30 |4| 2-3курс'),
    ('17:00', '17:00 |5| 2-3курс'),
    ('18:30', '18:30 |6| 2-3курс'),

    ('10:50', '10:50 |1| 1-4курс'),
    ('12:40', '12:40 |2| 1-4курс'),
    ('14:30', '14:30 |3| 1-4курс'),
    ('16:00', '16:00 |4| 1-4курс'),
    ('17:30', '17:30 |5| 1-4курс'),
    ('19:00', '19:00 |6| 1-4курс'),
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
        choices=start_time_choice,  # TODO: make editable.
    )
    end_time = models.CharField(
        verbose_name='End pair',
        max_length=5,
        choices=end_time_choice,
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
