import calendar

# Input commands:
SHOW = 'show'  # show current days remaining (optional)
LOG = 'log'  # print taken days off
ECHO = 'echo'  # print entire .vacationrc file
TAKE = 'take'  # take a day off ('take' is optional)
CANCEL = 'cancel'  # cancel a day off
SET = 'set'  # Set one of either rate or days
RATE = 'rate'  # Set current accumulation rate
DAYS = 'days'  # Fix number of days

# Token (output) commands:
TAKERANGE = 'takerange'
SETRATE = 'setrate'
SETDAYS = 'setdays'


def lex(args):
    """ Lex input and return a list of actions to perform. """
    if len(args) == 0 or args[0] == SHOW:
        return [(SHOW, None)]
    elif args[0] == LOG:
        return [(LOG, None)]
    elif args[0] == ECHO:
        return [(ECHO, None)]
    elif args[0] == SET and args[1] == RATE:
        return tokenizeSetRate(args[2:])
    elif args[0] == SET and args[1] == DAYS:
        return tokenizeSetDays(args[2:])
    elif args[0] == TAKE:
        return tokenizeTake(args[1:])
    elif args[0] == CANCEL:
        return tokenizeCancel(args[1:])
    elif isMonth(args[0]):
        return tokenizeTake(args)
    else:
        print('Unknown commands: {}'.format(' '.join(args)))
        return []  # No actions to perform


def tokenizeSetRate(args):
    if not args[0:]:
        raise ValueError('Missing args for <set rate>')
    try:
        rate = float(args[0])
    except ValueError:
        raise ValueError('Invalid rate: {}'.format(args))
    return [(SETRATE, '{}'.format(rate))]


def tokenizeSetDays(args):
    if not args[0:]:
        raise ValueError('Missing args for <set days>')
    try:
        days = float(args[0])
    except ValueError:
        raise ValueError('Invalid number of days: {}'.format(args))
    return [(SETDAYS, '{}'.format(days))]


def tokenizeTake(args):
    ret = [(TAKE, date) for date in lexDate(args)]
    return ret


def tokenizeCancel(args):
    ret = [(CANCEL, date) for date in lexDate(args)]
    return ret


def isMonth(arg):
    """ Determine if arg is in the calendar months, e.g. 'Jan' return True """
    month = arg[:3].capitalize()
    return month in calendar.month_abbr


def lexDate(args):
    month = args[0][:3].lower()
    if not isMonth(args[0]):
        raise ValueError('Not a valid month')
    dates = []
    for arg in args[1:]:
        day = getDay(arg)
        dates.append('{} {}'.format(month, day))
    return dates


def getDay(arg):
    arg = arg.strip(',')
    try:
        return int(arg)
    except ValueError:
        raise ValueError('Invalid day: {}'.format(arg))
