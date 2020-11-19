MIN_ABS_DIFFERENCE = 0
TRIGGER_DEAD_ZONE = 50
TRIGGER_RANGE = 550
STICK_DEAD_ZONE = 4000
STICK_RANGE = 32768

EVENT_MISC = 'Misc'
EVENT_SYNC = 'Sync'
EVENT_ABSOLUTE = 'Absolute'
EVENT_KEY = 'Key'

ignore_events = [EVENT_MISC, EVENT_SYNC]

EVENTS = {
    # Joysticks
    'ABS_X':'LSX',
    'ABS_Y': 'LSY',
    'ABS_RX': 'RSX',
    'ABS_RY': 'RSY',

    # Triggers
    'ABS_Z': 'LT',
    'ABS_RZ': 'RT',

    # DPad
    'ABS_HAT0X': 'DPADX',
    'ABS_HAT0Y': 'DPADY',

    # Face Buttons
    'BTN_NORTH': 'Y',
    'BTN_EAST': 'B',
    'BTN_SOUTH': 'A',
    'BTN_WEST': 'X',

    # Other buttons
    'BTN_THUMBL': 'LSZ',
    'BTN_THUMBR': 'RSZ',
    'BTN_TL': 'LB',
    'BTN_TR': 'RB',
    'BTN_MODE': 'XBOX',
    'BTN_START': 'START',
    'BTN_SELECT': 'MENU',
}

gamepad_state = {
    'LSX': 0.0,
    'LSY': 0.0,
    'RSX': 0.0,
    'RSY': 0.0,

    'LT': 0.0,
    'RT': 0.0,

    'DPADX': 0,
    'DPADY': 0,

    'Y': 0,
    'B': 0,
    'A': 0,
    'X': 0,

    'LSZ': 0,
    'RSZ': 0,
    'LB': 0,
    'RB': 0,
    'XBOX': 0,
    'START': 0,
    'MENU': 0
}