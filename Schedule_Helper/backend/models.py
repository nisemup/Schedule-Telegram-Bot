from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.crypto import get_random_string


days_choice = (
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('saturday', 'Saturday'),
)

faculty_choice = (
    ('Факультет економіки та управління', 'Економіка та уп.'),
    ('Факультет товарознавства, управління та сфери обслуговування', 'Товарознавство, уп. та сф. обсл.'),
    ('Факультет міжнародних економічних відносин та інформаційних технологій', 'МЕВ та ІТ'),
    ('Факультет права', 'Право')
)

rank_choice = (
    ('Ректор', 'Ректор'),
    ('Заступник ректора', 'Зас. ректора'),
    ('Декан', 'Декан'),
    ('Завідувач кафедри', 'Зав. кафедри'),
    ('Професор', 'Професор'),
    ('Доцент', 'Доцент'),
    ('Старший викладач', 'Ст. викладач'),
    ('Викладач', 'Викладач'),
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
        verbose_name = "Schedule"


class Lecturers(models.Model):
    first_name = models.CharField(
        max_length=35,
        verbose_name="First name"
    )

    last_name = models.CharField(
        max_length=35,
        verbose_name="Last name"
    )

    rank = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=rank_choice,
        verbose_name="Rank"
    )

    description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Description"
    )

    class Meta:
        verbose_name = 'Lecturer'

    def __str__(self):
        return self.first_name + " " + self.last_name


class Courses(models.Model):
    faculty = models.CharField(
        max_length=70,
        choices=faculty_choice,
        verbose_name="Faculty"
    )

    name = models.CharField(
        max_length=65,
        verbose_name="Name"
    )

    lecturers = models.ManyToManyField(Lecturers)

    deanery_location = models.CharField(
        max_length=60,
        verbose_name="Deanery location"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_courses'),
        ]
        verbose_name = 'Course'

    def __str__(self):
        return self.name


class Stats(models.Model):
    user = models.ForeignKey(
        Profiles,
        on_delete=models.CASCADE
    )

    button_name = models.CharField(
        verbose_name='Button name',
        max_length=35
    )

    count = models.SmallIntegerField(
        default=0,
        verbose_name='Count'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'button_name'],
                name='unique_stats'),
        ]
        verbose_name='Stat'