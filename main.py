from flet import *

def main(page: Page):

    logo_img = SafeArea(
        Image(
            src="/img/tany.png",
            width=300,
            height=100
        )
    )

    main_container = Container(
        expand=True,
        alignment=alignment.center,
        bgcolor="#E8D5DB",
        content=Column(
            controls=[
                logo_img
            ]
        )
    )

    page.title = "tany._nails"
    page.window_width = 400
    page.window_height = 700
    page.padding = 0
    page.add(main_container)
    page.update()


app(target=main,
    assets_dir="assets")
