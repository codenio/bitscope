#!/usr/bin/env python

from bitlib import *

class Trace:
    """Trace Class to handle trace related functionalities."""

    def trace(self, time_out, sync):
        """Commence capture subject to timeout T (seconds) and block until the
        trace completes unless A is true in which case return now and capture
        asynchronously. In the latter use BL_State() to determine the state of
        capture. Returns OK true if the trace commenced successfully, false
        otherwise. If T is zero or omitted, perform a forced trigger trace
        immediately. If T is negative, do the trace with infinite timeout but
        do it execute aysnchronously.

        :type time_out: double
        :param time_out: specify the time out for trace
        :type sync: BL_SYNC, BL_ASYNC
        :param sync: specify trace modes
        :return: boolean
        """
        return BL_Trace(time_out,sync)

    def rate(self,rate=None):
        """sets rate for trace.

        :type rate: int
        :param rate: rate to perform the trace
        :return: current rate
        """
        if rate is None:
            return BL_Rate()
        else:
            return BL_Rate(rate); # optional, default BL_MAX_RATE
    
    def size(self, size=None):
        """sets size for trace.

        :type size: int
        :param size: size to perform the trace
        :return: current size
        """
        if size is None:
            return BL_Size()
        else:
            return BL_Size(size); # optional default BL_MAX_SIZE
    
    def pre_capture(self, pre_capture=BL_ZERO):
        """sets pre_capture time for trace.

        :type pre_capture: int
        :param pre_capture: time to start capture before performing the trace
        :return: current pre_capture time
        """
        return BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
    
    def post_capture(self, post_capture=BL_ZERO):
        """sets post_capture time for trace.

        :type post_capture: int
        :param post_capture: time to stop capture after performing the trace
        :return: current post_capture time
        """
        return BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default

    def time(self, t=None):
        """sets time for trace.

        :type t: double
        :param t: time to trace
        :return: current time
        """
        if t is None:
            return BL_Time()
        else:
            return BL_Time(t)
    
    def trigger(self, volt, kind):
        """sets tigger for trace.

        :type volt: double
        :param volt: voltage level for trigger
        :type kind: BL_TRIG_RISE, BL_TRIG_FALL, BL_TRIG_HIGH, BL_TRIG_LOW, BL_TRIG_NONE
        :param kind: specify trigger type
        :return: cuurent trigger setting
        """
        if kind in [BL_TRIG_RISE, BL_TRIG_FALL, BL_TRIG_HIGH, BL_TRIG_LOW, BL_TRIG_NONE]:
            return BL_Trigger(volt,kind)

    def state(self):
        """returns current state of the machine.

        :return: current state of machine
        """
        return BL_State()

    def configure(self,rate=BL_MAX_RATE, size=BL_MAX_SIZE, pre_capture=BL_ZERO, post_capture=BL_ZERO):
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
        BL_Rate(rate); # optional, default BL_MAX_RATE
        BL_Size(size); # optional default BL_MAX_SIZE
        BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
        BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default
