from ..language import uk_UA as t
import datetime


days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']

day_translate = {
    days[0]: t.monday,
    days[1]: t.tuesday,
    days[2]: t.wednesday,
    days[3]: t.thursday,
    days[4]: t.friday,
    days[5]: t.saturday
}


def get_week_type():
    week = datetime.datetime.today().strftime("%U")
    return 'even' if int(week) % 2 == 0 else 'odd'


def create_pre(data):
    data = sorted(data)
    result = t.hi_pre + t.pre_form.format(
        data[0][2],
        data[0][5] if data[0][6] is None else f'<a href="{data[0][6]}">{data[0][5]}</a>',
        data[0][3],
        data[-1][4],
        len(data)
    ) + t.pre_footer

    return result


def create_schedule(data):
    result = {}
    for key in sorted(data):
        form = t.pairs_forms[key[1]].format(
            t.pair_name[key[1]],
            key[2],
            f'{key[3]} - {key[4]}',
            key[5] if key[6] is None else f'<a href="{key[6]}">{key[5]}</a>'
        )

        if result.get(key[0]):
            result[key[0]] += form
        else:
            result[key[0]] = form

    return result
