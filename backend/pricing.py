def calculate_price(settings):
    if settings.color and settings.duplex:
        rate = 15
    elif settings.color:
        rate = 10
    elif settings.duplex:
        rate = 3
    else:
        rate = 2

    total_pages = settings.pages * settings.copies
    return total_pages * rate
