import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


if __name__ == "__main__":
    from tgbot.bot import run_polling

    run_polling()
