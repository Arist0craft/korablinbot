from telegram import Update
from telegram.ext import CallbackContext

from utils import setup_logger
from ..utils.compute_manager import compute_client, ServiceError
from ..utils.minecraft_waiter import McWaiter, timeout

logger = setup_logger(__name__)


def start_server(u: Update, cct: CallbackContext):
    chat_id = u.effective_chat.id
    mc_waiter = McWaiter()
    try:
        if (
            compute_client.get_instance(compute_client.instance_id).data.lifecycle_state
            in ("STARTING", "RUNNING")
        ):
            logger.info("Instance already started")
            cct.bot.send_message(
                chat_id, "Сервер уже на старте или запущен. Проходи, не задерживайся."
            )

        else:
            cct.bot.send_message(chat_id, "Запускаем серверъ.")
            logger.info("Starting instance")
            res = compute_client.start_instance()
            if res:
                cct.bot.send_message(chat_id, "Осталось ещё немного... тебе АХАХАХАХ")
                logger.info("Instance successfully started")
                try:
                    logger.info("Waiting for Minecraft server query protocol status")
                    if mc_waiter.wait():
                        logger.info("Minecraft server successfully started")

                        cct.bot.send_message(
                            chat_id,
                            "Майнкрафт, курвобляджская пехота, я сказала стартуем!",
                        )
                except timeout as err:
                    cct.bot.send_message(
                        chat_id, "Сервачок не запустился, зовите Одмена, быро"
                    )
                    logger.exception(err)
                    raise err

            else:
                cct.bot.send_message(
                    chat_id, "Что-то пошло не так, бродяга, скажи Одмену"
                )
                logger.error("Something went wrong")

    except ServiceError as err:
        cct.bot.send_message(chat_id, "Что-то пошло не так, бродяга, скажи Одмену")
        logger.exception(err)
        raise err


def stop_server(u: Update, cct: CallbackContext):
    chat_id = u.effective_chat.id
    try:
        if (
            compute_client.get_instance(compute_client.instance_id).data.lifecycle_state
            in ("STOPPED", "STOPPING")
        ):
            logger.info("Instance already stopped")
            cct.bot.send_message(
                chat_id, "Сервер уже остановлен. Зачем ты это делаешь?"
            )
        else:
            cct.bot.send_message(chat_id, "Моя остановочка... (Серверъ).")
            logger.info("Stoping instance")
            res = compute_client.stop_instance()
            if res:
                cct.bot.send_message(chat_id, "Спасибо за игру, посоны")
                logger.info("Instance successfully stopped")
            else:
                cct.bot.send_message(
                    chat_id, "Сервак не остановился, минус все деньги, зовите Одмена"
                )
                logger.error("Instance wasn't stopped, smth went wrong")

    except ServiceError as err:
        cct.bot.send_message(chat_id, "Что-то пошло не так, бродяга, скажи Одмену")
        logger.exception(err)
        raise err
