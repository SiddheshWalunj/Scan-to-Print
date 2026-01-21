def generate_payment_payload(amount):
    # Later integrate PhonePe / GPay / Razorpay
    return f"upi://pay?pa=printer@upi&am={amount}&cu=INR"
