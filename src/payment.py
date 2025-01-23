from aiogram import Router, F, html
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

from config import STARS_AMOUNT, MESSAGES
from loader import bot

router = Router(name=__name__)


@router.message(Command("start"))
async def process_pay_command(message: Message) -> None:
    """
    Generate and send a payment invoice to the user.

    Args:
        message (Message): Incoming message with the command

    Sends:
        - Payment invoice for 1 Star
        - Error message if invoice creation fails
    """
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
        await message.answer("❌ <b>Failed to create payment invoice</b>")


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    """
    Validate the pre-checkout query before payment.

    Args:
        pre_checkout_query (PreCheckoutQuery): Pre-checkout query to validate
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message) -> None:
    """
    Process successful payment and send confirmation.

    Args:
        message (Message): Message containing successful payment info

    Sends:
        - Payment confirmation with transaction details
    """
    payment_info = message.successful_payment
    transaction_id = payment_info.telegram_payment_charge_id

    await message.answer(
        MESSAGES['payment_success'].format(
            amount=payment_info.total_amount,
            transaction_id=html.quote(transaction_id)
        )
    )
