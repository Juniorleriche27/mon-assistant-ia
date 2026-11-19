import asyncio
from app.koryxa_pay import koryxa_pay_client

async def main():
    try:
        res = await koryxa_pay_client.create_checkout(
            product_code="koryxa-assistant-ia",
            description="Pack Assistant IA",
            customer_id="test@koryxa.fr",
            amount_minor=11000,
            currency="XOF",
            idempotency_key="test-check-live-final-1"
        )
        print("RESULT_SUCCESS_URL:", res.get("checkout_url"))
        print("RESULT_PAYMENT_ID:", res.get("payment_id"))
        print("RESULT_STATUS:", res.get("payment_status"))
    except Exception as e:
        print("RESULT_ERROR:", e)

if __name__ == "__main__":
    asyncio.run(main())
