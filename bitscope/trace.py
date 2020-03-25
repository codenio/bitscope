#!/usr/bin/env python

from bitlib import *

class Trace:
    """
    """

    def trace(self, time_out, sync):
        return BL_Trace(time_out,sync)

    def rate(self,rate=None):
        if rate is None:
            return BL_Rate()
        else:
            return BL_Rate(rate); # optional, default BL_MAX_RATE
    
    def size(self, size=None):
        if size is None:
            return BL_Size()
        else:
            return BL_Size(size); # optional default BL_MAX_SIZE
    
    def pre_capture(self, pre_capture=BL_ZERO):
        return BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
    
    def post_capture(self, post_capture=BL_ZERO):
        return BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default

    def time(self, t=None):
        if t is None:
            return BL_Time()
        else:
            return BL_Time(t)
    
    def trigger(self, volt, kind):
        if kind in [BL_TRIG_RISE, BL_TRIG_FALL, BL_TRIG_HIGH, BL_TRIG_LOW, BL_TRIG_NONE]:
            return BL_Trigger(volt,kind)

    def state(self):
        return BL_State()

    def configure(self,rate=BL_MAX_RATE, size=BL_MAX_SIZE, pre_capture=BL_ZERO, post_capture=BL_ZERO):
        #Setup channel-nonspecific parameters for capture.
        BL_Rate(rate); # optional, default BL_MAX_RATE
        BL_Size(size); # optional default BL_MAX_SIZE
        BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
        BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default
