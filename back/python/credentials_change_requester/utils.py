def email_validate_function(email: str) -> bool:
    return email.find("@") != -1 and email.find(".") != -1 and email.find("@") < email.find(".")