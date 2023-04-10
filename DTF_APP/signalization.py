def red(text):
    return "\033[31m{}\033[0m".format(text)

def yellow(text):
    return "\033[33m{}\033[0m".format(text)

def blue(text):
    return "\033[34m{}\033[0m".format(text)

def green(text):
    return "\033[32m{}\033[0m".format(text)

def _info(*text):
    res = yellow('[LOG]') + ': '
    for word in text:
        res += blue(word) + ' '
    print(res)

def _success(*text):
    res = green('[SUCCESS]') + ' '
    for word in text:
        res += green(word)
    print(res)

def _error(*text):
    res = red('[ERROR]') + ': '
    for word in text:
        res += red(word) + ' '
    print(res)