from celery.utils.log import get_task_logger
from telegram import Update
from telegram.ext import CallbackContext

from ..utils.compute_manager import compute_client, ServiceError
from ..utils.minecraft_waiter import McWaiter, timeout

logger = get_task_logger(__name__)


def start_server(u: Update, cct: CallbackContext):
    chat_id = u.effective_chat.id
    mc_waiter = McWaiter()
    try:
        if compute_client.get_instance(
            compute_client.instance_id
        ).data.lifecycle_state in ("STARTING", "RUNNING"):
            logger.info("Instance already started")
            cct.bot.send_message(
                chat_id, "Сервер уже на старте или запущен. Проходи, не задерживайся."
            )
            return

        cct.bot.send_message(chat_id, "Запускаем серверъ.")
        logger.info("Starting instance")
        res = compute_client.start_instance()
        if not res:
            cct.bot.send_message(chat_id, "Что-то пошло не так, бродяга, скажи Одмену")
            logger.error("Something went wrong, instance wasn't started")
            return

        cct.bot.send_message(chat_id, "Осталось ещё немного... тебе АХАХАХАХ")
        logger.info("Instance successfully started")

        if not mc_waiter.wait():
            cct.bot.send_message(chat_id, "Что-то пошло не так, бродяга, скажи Одмену")
            logger.error("Something went wrong, MC Server wasn't started")
            return

        logger.info("Minecraft server successfully started")
        cct.bot.send_message(
            chat_id,
            "Майнкрафт, курвобляджская пехота, я сказала стартуем!",
        )
    except ServiceError as err:
        cct.bot.send_message(chat_id, "Что-то пошло не так, бродяга, скажи Одмену")
        logger.exception(err)
        raise err

    except timeout as err:
        cct.bot.send_message(chat_id, "Сервачок не запустился, зовите Одмена, быро")
        logger.exception(err)
        raise err


def stop_server(u: Update, cct: CallbackContext):
    chat_id = u.effective_chat.id
    try:
        if compute_client.get_instance(
            compute_client.instance_id
        ).data.lifecycle_state in ("STOPPED", "STOPPING"):
            logger.info("Instance already stopped")
            cct.bot.send_message(
                chat_id,
                "Сервер уже останавливается или остановлен. Зачем ты это делаешь?",
            )
            return

        cct.bot.send_message(chat_id, "Моя остановочка... (Серверъ).")
        logger.info("Stoping instance")
        res = compute_client.stop_instance()
        if not res:
            cct.bot.send_message(
                chat_id, "Сервак не остановился, минус все деньги, зовите Одмена"
            )
            logger.error("Instance wasn't stopped, smth went wrong")
            return

        cct.bot.send_message(chat_id, "Спасибо за игру, посоны")
        logger.info("Instance successfully stopped")

    except ServiceError as err:
        cct.bot.send_message(chat_id, "Что-то пошло не так, бродяга, скажи Одмену")
        logger.exception(err)
        raise err
