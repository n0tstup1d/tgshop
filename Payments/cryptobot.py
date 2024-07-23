from aiocryptopay import AioCryptoPay, Networks
import asyncio
import config


async def create_crypto_instance():
    crypto = AioCryptoPay(token=config.crypto_token, network=Networks.MAIN_NET)
    return crypto


async def order(summ, asset):
    crypto = await create_crypto_instance()
    amount = await crypto.get_amount_by_fiat(summ=summ, asset=asset, target='RUB')
    invoice = await crypto.create_invoice(asset=asset, amount=amount)
    print(invoice.bot_invoice_url)
    return invoice.bot_invoice_url,invoice.invoice_id


async def check_status(summ, id_pay):
    crypto = await create_crypto_instance()
    old_invoice = await crypto.get_invoices(invoice_ids=id_pay)
    return old_invoice[0].status


