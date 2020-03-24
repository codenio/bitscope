#!/usr/bin/env python

from bitlib import *

class Channel:

    id = ""
    device = ""
    src = ""
    analog_count = ""
    logic_count = ""
    analog_range_count = ""

    def __init__(self, device, channel):
        
        self.device = device
        self.id = channel
        # device is seleted from previous Device class
        # select corresponding channel
        BL_Select(BL_SELECT_CHANNEL,channel)
        self.analog_count = BL_Count(BL_COUNT_ANALOG)
        self.logic_count = BL_Count(BL_COUNT_LOGIC)
        self.analog_range_count = BL_Count(BL_COUNT_RANGE)

    def select(self):
        # check if the corresponding device is already selected
        if self.device != BL_Select(BL_SELECT_DEVICE,BL_ASK):
            # select the corresponding device first
            BL_Select(BL_SELECT_DEVICE,self.device)
        
        if self.id != BL_Select(BL_SELECT_CHANNEL,BL_ASK):
            # select the corresponding channel next
            BL_Select(BL_SELECT_CHANNEL,self.id)
        
        # print "Selected Device : {} , Channel : {}".format(self.device,self.id)

    def configure(self, source=BL_SOURCE_BNC, offset=BL_ZERO,analog_range=0,coupling=BL_COUPLING_DC):
        
        self.select()
        if source in [BL_SOURCE_POD, BL_SOURCE_BNC, BL_SOURCE_X10, BL_SOURCE_X20, BL_SOURCE_X50, BL_SOURCE_ALT, BL_SOURCE_GND]:
            # select the corresponding source for the channel
            BL_Select(BL_SELECT_SOURCE,source)
            self.source = source
            
        # set offset
        BL_Offset(offset)
        # set range
        if analog_range >= 0 and analog_range <= (self.analog_range_count)-1:
            BL_Range(analog_range)
        # set coupling
        if coupling in [BL_COUPLING_AC,BL_COUPLING_DC,BL_COUPLING_RF]:
            BL_Coupling(coupling)

    # enable channel
    def enable(self):
        self.select()
        BL_Enable(1)
        print "Enabled Device : {} , Channel : {}".format(self.device,self.id)

    # disable channel
    def disable(self):
        self.select()   
        BL_Enable(0)
        print "Disabled Device : {} , Channel : {}".format(self.device,self.id)

    # acquire data from channel
    def acquire(self):
        self.select()
        print "Acquiring Data from Device : {} , Channel : {}".format(self.device,self.id)
        return BL_Acquire()


