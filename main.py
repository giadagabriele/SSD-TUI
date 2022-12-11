from rich.console import Console

from domains.dress_shop.app import *
from settings import settings


def main(name: str):
    console = Console()

    if settings['DEBUG'] == 'True':
        for key in settings:
            console.print(f"{key}={settings[key]}")

    if name == '__main__':
        App().run()


main(__name__)
