"""
Bitscope Wrapper Library 0.2 

This is an object-oriented wrapper for BitScope Library API 2.0.
which is a programming library for all current model BitScopes.

It abstracts the BitScope Virtual Machine into a functional API that
supports connecting to BitScope, setting up trigger conditions,
performing a waveform capture and acquiring captured data as well as
more specialized functions such as generating signals and capturing
continuous waveforms.

BitScopes capture signals in various modes (see scope.mode()) but all modes
are programmed in a similar multi-phase manner:
 
    Open -> Setup -> Trace -> Acquire -> Close
 
Initialise using scope.open() or Scope() class (scope.initialize() is optional).
 
Setup is the most detailed phase and uses a selection of scope.devices[].select()
or scope.devices[].channels[].select().

BL_Mode, BL_Offset, BL_Enable, BL_Rate,
BL_Time, BL_Size BL_Intro and BL_Trigger.
 
Trace performs the actual data capture via scope.tracer.trace().
 
Acquire reads the captured data from the device channel by channel and
uses scope.devices[].channels[].acquire().

which may be imported directly, e.g.::

    import bitscope

    or 

    from bitscope import *

Modules include:

    :mod:`bitscope.scope`
        defines the :class:`~bitscope.scope.Scope` class.

    :mod:`bitscope.device`
        defines the :class:`~bitscope.device.Device` class.

    :mod:`bitscope.channel`
        defines the :class:`~bitscope.channel.Channel` class.

    :mod:`bitscope.trace`
        defines the :class:`~bitscope.trace.Trace` class.

    :mod:`bitscope.metadata`

"""
from bitscope.scope import Scope
from bitscope.metadata import __name__,__version__,__status__,__license__


class Source:
    """Source Class for Holding Constants.
    Available Options can be accessed as

    SOURCE.POD - analog or logic channel POD input
    SOURCE.BNC - analog channel BNC input (if available)
    SOURCE.X10 - analog input prescaled by 10
    SOURCE.X20 - analog input prescaled by 20
    SOURCE.X50 - analog input prescaled by 50
    SOURCE.ALT - alternate input (data acquisition)
    SOURCE.GND - ground reference input
    """

    POD = 0
    BNC = 1
    X10 = 2
    X20 = 3
    X50 = 4
    ALT = 5
    GND = 6

SOURCE = Source()

class Mode:
    """Mode Class for Holding Constants.
    Available Options can be accessed as

    MODE.FAST - analog capture at the fastest rates available
    MODE.DUAL - dual channel sample synchronous analog capture
    MODE.MIXED - mixed analog + logic signal capture
    MODE.LOGIC - logic only capture mode
    MODE.STREAM - streaming mixed signal capture
    """

    FAST = 0
    DUAL = 1
    MIXED = 2
    LOGIC = 3
    STREAM = 4

MODE = Mode()

class Count:
    """Count Class for Holding Constants.
    Available Options can be accessed as

    COUNT.DEVICE - successfully opened devices
    COUNT.ANALOG - analog channels on the selected device
    COUNT.LOGIC - logic channels on the selected device
    COUNT.RANGE - number of analog ranges on the selected channel
    """
    
    DEVICE = 0
    ANALOG = 1
    LOGIC = 2
    RANGE = 3

COUNT = Count()

class Coupling:
    """Coupling Class for Holding Constants.
    Available Options can be accessed as

    COUPLING.DC - direct connection for DC signals (the default)
    COUPLING.AC - AC connection (eliminates DC bias)
    COUPLING.RF - RF connection for very high frequencies
    """

    DC = 0
    AC = 1
    RF = 2

COUPLING = Coupling()

class Max:
    """Max Class for Holding Constants.
    Available Options can be accessed as
    
    MAX.RATE - specify to choose the highest sample rate supported by the selected device in the current mode.
    MAX.SIZE - specify to choose the largest size supported by the selected device in the current mode.
    """

    RATE = 0
    SIZE = 0
    TIME = 0

MAX = Max()

class Select:
    """Max Class for Holding Constants.
    Available Options can be accessed as
    
    SELECT.DEVICE - select a device
    SELECT.CHANNEL - select a channel on the (previously) selected device
    SELECT.SOURCE - select an input source of the selected channel
    """

    DEVICE = 0
    CHANNEL = 1
    SOURCE = 2

SELECT = Select()

class State:
    """Max Class for Holding Constants.
    Available Options can be accessed as
    
    STATE.IDLE - idle and ready to program
    STATE.ACTIVE - actively capturing data
    STATE.DONE - completed capturing data successfully
    STATE.ERROR - completed capturing data unsuccessfully
    """

    ACTIVE = 1
    DONE = 2
    ERROR = 3
    IDLE = 0

STATE = State()

class Trace:
    """Max Class for Holding Constants.
    Available Options can be accessed as
    
    TRACE.FORCED - commence immediately regardless of the trigger
    TRACE.FOREVER - commence and wait for the trigger, possibly forever.
    TRACE.SYNCHRONOUS - to start the trace synchronously
    TRACE.ASYNCHRONOUS - to start the trace asynchronously
    """

    SYNCHRONOUS = 0
    ASYNCHRONOUS = 1

    FORCED = 0
    FOREVER = -1

TRACE = Trace()

class Trigger:
    """Max Class for Holding Constants.
    Available Options can be accessed as
    
    TRIGGER.RISE - To start capture during Rise of the trigger
    TRIGGER.FALL - To start capture during Fall of the trigger
    TRIGGER.HIGH - To start capture when trigger becomes High
    TRIGGER.LOW - To start capture when trigger becomes Low
    TRIGGER.NONE - No trigger configured
    """

    RISE = 0
    FALL = 1
    HIGH = 2
    LOW = 3
    NONE = 4

TRIGGER = Trigger()

class Version:
    """Max Class for Holding Constants.
    Available Options can be accessed as
    
    VERSION.DEVICE - device model and version identifier
    VERSION.LIBRARY - library version and production build ID
    VERSION.BINDING - language binding and version
    """

    DEVICE = 0
    LIBRARY = 1
    BINDING = 2

VERSION = Version()


class Layer:
    """Layer Class for Holding Constants.
    Available Options can be accessed as

    LAYER.SCOPE - to select the layer as SCOPE
    LAYER.GENERATOR - to select the layer as GENERATOR
    """
    SCOPE = 0
    GENERATOR = 1

LAYER = Layer() 

ASK = -1
ZERO = 0