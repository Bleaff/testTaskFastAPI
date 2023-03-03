def red(text):
    return "\033[31m{}\033[0m".format(text)

def yellow(text):
    return "\033[33m{}\033[0m".format(text)

def blue(text):
    return "\033[34m{}\033[0m".format(text)

def _info(text):
    print(f"{yellow('[LOG]')}:{blue(text)}")

def _error(text):
    print(f"{red('[ERROR]')}: {red(text)}")
