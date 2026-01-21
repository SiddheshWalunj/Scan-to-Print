from backend.pricing import calculate_price
from backend.payment import generate_payment_payload
from backend.printer import send_to_printer

def process_print_job(file, settings):
    amount = calculate_price(settings)
    payment_qr_data = generate_payment_payload(amount)
    return amount, payment_qr_data

def confirm_and_print(file, settings):
    return send_to_printer(file, settings)
