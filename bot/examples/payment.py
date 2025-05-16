from aiogram import Router, F, html, Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from bot.utils import PAYMENT_SUCCESS, PAYMENT_ERROR
from config import STARS_AMOUNT

router = Router(name=__name__)


@router.message(Command("start"))
async def process_pay_command(message: Message, bot: Bot) -> None:
    try:
        prices = [LabeledPrice(label='Stars Payment', amount=STARS_AMOUNT)]
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Stars Payment Example',
            description='Payment for services via Stars.',
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter='stars-payment',
            payload='stars-payment-payload'
        )
        await message.delete()
    except TelegramAPIError:
        await message.answer(PAYMENT_ERROR)


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message) -> None:
    payment_info = message.successful_payment
    transaction_id = payment_info.telegram_payment_charge_id

    await message.answer(
        PAYMENT_SUCCESS.format(
            amount=payment_info.total_amount,
            transaction_id=html.quote(transaction_id)
        )
    )
