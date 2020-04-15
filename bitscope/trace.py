#!/usr/bin/env python

import bitlib

class Trace:
    """Trace Class to handle trace related functionalities."""

    def trace(self, time_out=0, sync=False):
        """Commence capture subject to time_out (seconds) and block until the
        trace completes unless sync is true in which case return now and capture
        asynchronously. In the latter use scope.tracer.state() to determine the state of
        capture. Returns OK true if the trace commenced successfully, false
        otherwise. If time_out is zero or omitted, perform a forced trigger trace
        immediately. If time_out is negative, do the trace with infinite timeout but
        do it execute aysnchronously.

        :type time_out: double
        :param time_out: specify the time out for trace
        :type sync: bitlib.BL_SYNC, bitlib.BL_ASYNC
        :param sync: specify trace modes
        
        :return: boolean
        """
        return bitlib.BL_Trace(time_out,sync)

    def rate(self,rate=None):
        """sets rate for trace.

        :type rate: int
        :param rate: rate to perform the trace
        :return: current rate
        """
        if rate is None:
            return bitlib.BL_Rate()
        else:
            return bitlib.BL_Rate(rate); # optional, default bitlib.BL_MAX_RATE
    
    def size(self, size=None):
        """sets size for trace.

        :type size: int
        :param size: size to perform the trace
        :return: current size
        """
        if size is None:
            return bitlib.BL_Size()
        else:
            return bitlib.BL_Size(size); # optional default bitlib.BL_MAX_SIZE
    
    def pre_capture(self, pre_capture=bitlib.BL_ZERO):
        """sets pre_capture time for trace.
        Request pretrigger hold-off duration pre_capture (in seconds) and return duration
        A that will actually be used. They are usually the same but may differ
        depending on the capabilities of the connected device.

        :type pre_capture: int
        :param pre_capture: time to start capture before performing the trace
        :return: current pre_capture time
        """
        return bitlib.BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
    
    def post_capture(self, post_capture=bitlib.BL_ZERO):
        """sets post_capture time for trace.
        
        Assigned post_capture (seconds) as the post-triger delay. If S is 0 or omitted, disables delay.

        :type post_capture: int
        :param post_capture: time to stop capture after performing the trace
        :return: current post_capture time
        """
        return bitlib.BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default

    def time(self, t=None):
        """sets time for trace.

        :type t: double
        :param t: time to trace
        :return: current time
        """
        if t is None:
            return bitlib.BL_Time()
        else:
            return bitlib.BL_Time(t)
    
    def trigger(self, volt, kind):
        """sets tigger for trace.
        Assign volt (volts) as the trigger level on edge kind (0=>rise, 1=>fall).

        :type volt: double
        :param volt: voltage level for trigger
        :type kind: int
        Available Options can be accessed as

        TRIGGER.RISE - To start capture during Rise of the trigger
        TRIGGER.FALL - To start capture during Fall of the trigger
        TRIGGER.HIGH - To start capture when trigger becomes High
        TRIGGER.LOW - To start capture when trigger becomes Low
        TRIGGER.NONE - No trigger configured
        :param kind: specify trigger type
        
        :returns: cuurent trigger setting
        """
        if kind in [bitlib.BL_TRIG_RISE, bitlib.BL_TRIG_FALL, bitlib.BL_TRIG_HIGH, bitlib.BL_TRIG_LOW, bitlib.BL_TRIG_NONE]:
            return bitlib.BL_Trigger(volt,kind)

    def state(self):
        """returns current state of the machine.

        :return: current state of machine
        """
        return bitlib.BL_State()

    def configure(self,rate=bitlib.BL_MAX_RATE, size=bitlib.BL_MAX_SIZE, pre_capture=bitlib.BL_ZERO, post_capture=bitlib.BL_ZERO):
        """configure the trace settings.

        :type rate: int
        :param rate: rate to perform the trace
        :type size: int
        :param size: size to perform the trace
        :type pre_capture: int
        :param pre_capture: time to start capture before performing the trace
        :type post_capture: int
        :param post_capture: time to stop capture after performing the trace
        """
        #Setup channel-nonspecific parameters for capture.
        bitlib.BL_Rate(rate); # optional, default bitlib.BL_MAX_RATE
        bitlib.BL_Size(size); # optional default bitlib.BL_MAX_SIZE
        bitlib.BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
        bitlib.BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default