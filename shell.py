import pickle
import itertools

from interfaces.web_app.selenium._app import initialize as _initialize
from config import build_use_cases as _build_use_cases


def initialize(headless=True):
    return _initialize(headless)


def build_use_cases(driver):
    return _build_use_cases(driver)


def save_driver(driver):
    with open('driver.pickle', 'wb') as fp:
        pickle.dump(driver, fp)


def load_driver():
    with open('driver.pickle', 'rb') as fp:
        return pickle.load(fp)


def get_user_input():

    for i in itertools.count():
        try:
            yield i, input('In [%d]: ' % i)
        except KeyboardInterrupt:
            pass
        except EOFError:
            break


def exec_function(user_input):

    try:
        compile(user_input, '<stdin>', 'eval')
    except SyntaxError:
        return exec
    return eval


def exec_user_input(i, user_input, user_globals):

    user_globals = user_globals.copy()
    try:
        retval = exec_function(user_input)(
            user_input, user_globals
        )
    except Exception as e:
        print('%s: %s' % (e.__class__.__name__, e))
    else:
        if retval is not None:
            print('Out [%d]: %s' % (i, retval))
    return user_globals


def selected_user_globals(user_globals):

    return (
        (key, user_globals[key])
        for key in sorted(user_globals)
        if not key.startswith('__') or not key.endswith('__')
    )


def main():

    user_globals = {}
    for i, user_input in get_user_input():
        user_globals = exec_user_input(
            i, user_input, user_globals
        )


if __name__ == '__main__':
    main()
