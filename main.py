from flet import *
import datetime
import calendar
import locale
from calendar import HTMLCalendar
from dateutil import relativedelta
import time

locale.setlocale(locale.LC_TIME, 'uk_UA')


def main(page: Page):

    today = datetime.datetime.today()
    page.session.set("current_month", today.month)
    page.session.set("current_day", today.day)
    page.session.set("current_year", today.year)

    def get_next(e):
        current_month = page.session.get("current_month")
        current_day = page.session.get("current_day")
        current_year = page.session.get("current_year")

        current = datetime.date(current_year, current_month, current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month

        page.session.set("current_month", next_month.month)
        page.session.set("current_day", next_month.day)
        page.session.set("current_year", next_month.year)

        calendar_main()
        main_container.update()

    def get_prev(e):
        current_month = page.session.get("current_month")
        current_day = page.session.get("current_day")
        current_year = page.session.get("current_year")

        current = datetime.date(current_year, current_month, current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month

        page.session.set("current_month", next_month.month)
        page.session.set("current_day", next_month.day)
        page.session.set("current_year", next_month.year)

        calendar_main()
        main_container.update()

    def open_date(e):
        if e.control.bgcolor == "#D41215":
            pass
        else:
            e.control.bgcolor = colors.WHITE24
            e.control.update()
            time.sleep(0.1)
            e.control.bgcolor = colors.TRANSPARENT
            e.control.update()
        # day_num = e.control.data
        page.session.set("day_num", e.control.data)
        print(page.session.get("day_num"))
        page.dialog = open_date_menu
        open_date_menu.open = True
        page.update()

    def touch(e):
        if e.control.bgcolor == "#D41215":
            pass
        else:
            if e.data == "true":
                e.control.bgcolor = colors.WHITE24
                e.control.update()
            else:
                e.control.bgcolor = colors.TRANSPARENT
                e.control.update()

    def calendar_main():
        current_month = page.session.get("current_month")
        current_day = page.session.get("current_day")
        current_year = page.session.get("current_year")
        cal = HTMLCalendar()
        current_calendar = cal.monthdayscalendar(current_year, current_month)
        formatted_month_name = calendar.month_name[current_month].capitalize()
        str_date = '{0} {1}, {2}'.format(
            formatted_month_name, current_day, current_year)
        date_display = Text(str_date, text_align='center',
                            size=20, color="black", weight="w500", font_family="Golos Text")
        next_button = Container(
            Text('>', text_align='right', size=20, color="black"), on_click=get_next)
        div = Divider(height=1, thickness=1.0)
        prev_button = Container(
            Text('<', text_align='left', size=20, color="black"), on_click=get_prev)
        calendar_column = Column([Row([prev_button, date_display, next_button], alignment=MainAxisAlignment.SPACE_EVENLY,
                                  vertical_alignment=CrossAxisAlignment.CENTER, height=40, expand=False), div],
                                 spacing=2, width=355, height=330, alignment=MainAxisAlignment.START, expand=False)

        weekday_name = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]

        week_days_row = Row(alignment=MainAxisAlignment.CENTER)
        for day_name in weekday_name:
            week_days_row.controls.append(Container(
                content=Text(day_name[:3], size=15, color="black",
                             weight="w500", font_family="Golos Text"),
                width=40, height=30, alignment=alignment.center,
                border_radius=border_radius.all(0),
                bgcolor=colors.TRANSPARENT
            ))
        calendar_column.controls.append(week_days_row)

        for week in current_calendar:
            week_row = Row(alignment=MainAxisAlignment.CENTER)
            for day in week:
                if day > 0:
                    is_current_day_font = FontWeight.W_300
                    is_current_day_bg = colors.TRANSPARENT
                    display_day = str(day)
                    if len(str(display_day)) == 1:
                        display_day = '0%s' % display_day

                    if day == current_day and current_month == today.month and current_year == today.year:
                        is_current_day_font = FontWeight.BOLD
                        is_current_day_bg = "#D41215"

                    day_button = Container(content=Text(str(display_day), weight=is_current_day_font, color="black", font_family="Golos Text"),
                                           on_click=open_date, on_hover=lambda e: touch(e), data=(
                                           current_month, day, current_year),
                                           width=40, height=40, alignment=alignment.center,
                                           border_radius=border_radius.all(20),
                                           border=border.all(
                                               2, is_current_day_bg))
                else:
                    day_button = Container(
                        width=40, height=40, border_radius=border_radius.all(15))
                week_row.controls.append(day_button)
            calendar_column.controls.append(week_row)
        calendar_container.content = calendar_column
        return calendar_container

    open_date_menu = AlertDialog(
        content_padding=0,
        # inset_padding=0,
        actions_padding=0,
        content=Container(
            alignment=alignment.center,
            blur=10,
            border_radius=25,
            expand=True,
            gradient=LinearGradient(
                begin=alignment.top_center,
                end=alignment.bottom_center,
                colors=["#E8D5DB", '#ff6666'],
            ),
            content=Column(
                controls=[
                    Text("Кохаю Тетян!",
                         size=25,
                         color='black')
                ]
            )
        )
    )

    calendar_container = Container(
        blur=10,
        bgcolor=colors.BLACK12,
        border_radius=15,
    )

    logo_img = SafeArea(
        Image(
            src="/img/tany_logo.png",
            width=300,
            height=150
        )
    )

    main_container = Container(
        gradient=LinearGradient(
            begin=alignment.top_center,
            end=alignment.bottom_center,
            colors=["#E8D5DB", '#ff6666']
        ),
        expand=True,
        padding=15,
        alignment=alignment.center,
        # bgcolor="#E8D5DB",
        content=Column(
            horizontal_alignment='center',
            controls=[
                logo_img,
                calendar_container
            ]
        )
    )

    page.fonts = {
        "Golos Text": "/fonts/GolosText.ttf"
    }
    page.title = "tany._nails"
    page.window_width = 400
    page.window_height = 700
    page.padding = 0
    page.add(main_container)
    calendar_main()
    page.update()


app(target=main,
    assets_dir="assets")
