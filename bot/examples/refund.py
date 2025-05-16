from aiogram import Router, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.methods.refund_star_payment import RefundStarPayment
from aiogram.types import Message

from bot.utils import INVALID_COMMAND, REFUND_SUCCESS, REFUND_FAIL

router = Router(name=__name__)


@router.message(Command("refund"))
async def process_refund(message: Message, bot: Bot) -> None:
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer(INVALID_COMMAND)
        await message.delete()
        return

    transaction_id = parts[1]
    try:
        result = await bot(RefundStarPayment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        ))

        await message.answer(
            REFUND_SUCCESS if result else REFUND_FAIL
        )
        await message.delete()
    except TelegramAPIError:
        await message.answer(REFUND_FAIL)
        await message.delete()
