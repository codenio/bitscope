#!/usr/bin/env python

import bitlib
from bitscope.channel import Channel

from utils.logger import logger

class Device:
    """Device class to select and configure devices that are open."""
    name = None
    id = None
    mode = None
    version = None
    channels = None

    def __init__(self,device):
        """Initialise the Device Object.

        :type device: int
        :param device: device id to be initialised
        
        :returns: instance of the class Device
        """
        self.id = device
        bitlib.BL_Select(bitlib.BL_SELECT_DEVICE,device)
        self.name = bitlib.BL_Name()
        self.device_id = bitlib.BL_ID()
        self.version = bitlib.BL_Version(bitlib.BL_VERSION_DEVICE)
        # Find number of channels in each device and create Channel object for each and append in devices.channels
        self.channels = []
        for channel in range(0,bitlib.BL_Count(bitlib.BL_COUNT_ANALOG)):
            self.channels.append(Channel(self.id, channel))
        for channel in range(0,bitlib.BL_Count(bitlib.BL_COUNT_LOGIC)):
            self.channels.append(Channel(self.id, channel))
    
    def select(self):
        """Request the selection of a current device.

        :return: current selection is returned.
        """
        # check if the required device is selected
        if self.id != bitlib.BL_Select(bitlib.BL_SELECT_DEVICE,bitlib.BL_ASK):
            # select the corresponding device first
            self.id = bitlib.BL_Select(bitlib.BL_SELECT_DEVICE,self.id)
        
        return self.id
    
    def mode(self, mode):
        """Assign mode to the selected device and return the mode if
        successful.

        :type mode: int
        :param mode: Assign mode. 
        Available Options can be accessed as
        
        MODE.FAST - analog capture at the fastest rates available
        MODE.DUAL - dual channel sample synchronous analog capture
        MODE.MIXED - mixed analog + logic signal capture
        MODE.LOGIC - logic only capture mode
        MODE.STREAM - streaming mixed signal capture
        
        :return: return the mode if successful
        """
        self.select()
        if mode in [bitlib.BL_MODE_FAST, bitlib.BL_MODE_DUAL, bitlib.BL_MODE_MIXED, bitlib.BL_MODE_LOGIC, bitlib.BL_MODE_STREAM]:
            # select the mode
            bitlib.BL_Mode(mode)
            self.mode = mode
            logger.debug("Device : {} set to Mode : {}".format(self.id,self.mode))
        
        return self.mode