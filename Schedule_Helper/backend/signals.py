from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Schedule


@receiver(pre_save, sender=Schedule)
def set_start_end_time(sender, instance, **kwargs):
    course_number = int(str(instance.group.gnum)[0])
    number = instance.number

    time_mapping = {
        (1, 1): ('09:30', '10:50'),
        (1, 2): ('11:20', '12:40'),
        (1, 3): ('13:10', '14:30'),
        (1, 4): ('14:40', '16:00'),
        (1, 5): ('16:10', '17:30'),
        (1, 6): ('17:40', '19:00'),

        (4, 1): ('09:30', '10:50'),
        (4, 2): ('11:20', '12:40'),
        (4, 3): ('13:10', '14:30'),
        (4, 4): ('14:40', '16:00'),
        (4, 5): ('16:10', '17:30'),
        (4, 6): ('17:40', '19:00'),

        (2, 1): ('09:00', '10:20'),
        (2, 2): ('10:50', '12:10'),
        (2, 3): ('12:40', '14:00'),
        (2, 4): ('14:10', '15:30'),
        (2, 5): ('15:40', '17:00'),
        (2, 6): ('17:10', '18:30'),

        (3, 1): ('09:00', '10:20'),
        (3, 2): ('10:50', '12:10'),
        (3, 3): ('12:40', '14:00'),
        (3, 4): ('14:10', '15:30'),
        (3, 5): ('15:40', '17:00'),
        (3, 6): ('17:10', '18:30'),
    }

    if (course_number, number) in time_mapping:
        start_time, end_time = time_mapping[(course_number, number)]
        instance.start_time = start_time
        instance.end_time = end_time