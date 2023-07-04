from faker import Faker
import json_log_formatter
import logging, sys
import random
import time

# Logger configuration.
formatter = json_log_formatter.JSONFormatter()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Fake data generator.
fake = Faker()


def log_checkout_transaction():
    # 0. Generate a transaction ID.
    transaction_id = fake.uuid4()

    # 1. Gather shipping details.
    shipping_details = {
        "address": fake.address(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "transaction_id": transaction_id,
    }
    logging.info(
        "🏠 Shipping details.",
        extra=shipping_details,
    )
    time.sleep(random.uniform(1.0, 2.0))

    # 2. Gather card details.
    SUPPORTED_CARDS = ["visa", "mastercard"]
    card_type = SUPPORTED_CARDS[random.randint(0, 1)]
    card_details = {
        "credit_card_expire": fake.credit_card_expire(),
        "credit_card_number": fake.credit_card_number(card_type),
        "credit_card_provider": card_type,
        "credit_card_security_code": fake.credit_card_security_code(card_type),
        "transaction_id": transaction_id,
    }
    logging.info(
        "💳 Card details.",
        extra=card_details,
    )
    time.sleep(random.uniform(1.0, 2.0))

    # 3. Validated details.
    logging.info(
        "✅ Successful checkout.",
        extra={
            **shipping_details,
            **card_details,
            "transaction_id": transaction_id,
        },
    )


if __name__ == "__main__":
    while True:
        log_checkout_transaction()
        time.sleep(random.uniform(0.0, 3.0))
