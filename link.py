import time
#simulat typing of both password and email fields
def simulate_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)