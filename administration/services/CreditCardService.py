from django.core.exceptions import ValidationError


def get_cc_type(number):
    """
    Gets credit card type given number. Based on values from Wikipedia page
    "Credit card number".
    <a href="http://en.wikipedia.org/w/index.php?title=Credit_card_number
">http://en.wikipedia.org/w/index.php?title=Credit_card_number
</a>    """
    number = str(number)
    #group checking by ascending length of number
    if len(number) == 13:
        if number[0] == "4":
            return "Visa"
    elif len(number) == 14:
        if number[:2] == "36":
            return "MasterCard"
    elif len(number) == 15:
        if number[:2] in ("34", "37"):
            return "American Express"
    elif len(number) == 16:
        if number[:4] == "6011":
            return "Discover"
        if number[:2] in ("51", "52", "53", "54", "55"):
            return "MasterCard"
        if number[0] == "4":
            return "Visa"
    elif len(number) == 19:
        if number[0] == "4":
            return "Visa"
    return "Unknown"

def luhn(input):
    if not input.isdigit():
        raise ValidationError(
            ('%(input)s no es un N. de tarjeta de credito correcto'),
            params={'input': input},
        )
    digits = [int(c) for c in input if c.isdigit()]
    checksum = digits.pop()
    digits.reverse()
    doubled = [2*d for d in digits[0::2]]
    total = sum(d-9 if d > 9 else d for d in doubled) + sum(digits[1::2])
    if (total * 9) % 10 != checksum:
        raise ValidationError(
            ('%(input)s no es un N. de tarjeta de credito correcto'),
            params={'input': input},
        )
