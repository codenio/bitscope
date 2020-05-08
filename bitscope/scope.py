#!/usr/bin/env python

import bitlib

from bitscope.device import Device
from bitscope.channel import Channel
from bitscope.trace import Trace as Tracer

from utils.logger import logger

class Scope:
    """scope class to open bitscope modules connected to pc.
    """
    # devices list to hold Device Objects for Opened Devises.
    devices = []
    
    # tracer attribute to hold tracer Object
    tracer = None
    
    def __init__(self, probe_files=None, count=1):
        """Initialise the Scope Object.
        
        Open devices listed in probe file probe_files (string) or a literal list of links,
        also specified via probe_files (individual links are separated by newlines). If
        not specified, the standard probe file is used. Opens the first valid
        link found unless count is specified in which case count links are attempted and
        valid links are opened. Returns number of successfully opened links.

        Initializes Device Objects for each opened device
        Initializes Channel Objects for each channel available in the device.
        
        :type probe_files: string
        :param probe_files: USB Port Connected to Bitscope
        :type count: int
        :param count: number of devices to be opened. default 1
        
        :returns: instance of the class Scope  
        """
         
        # Finds number of Devices Opened
        self.device_count = bitlib.BL_Open(probe_files,count)
        
        if self.device_count == 0:
            logger.debug("  FAILED: no devices found (check your probe file).")
            return
        
        # create Device object for each and append in scope.devices
        self.devices = [ Device(device) for device in range(0,bitlib.BL_Count(bitlib.BL_COUNT_DEVICE))] 
        
        # number of corresponding channels
        # instanciate Object from Sub Classess 
        self.tracer = Tracer()
        logger.debug("Bitscope Micro Units Opened : {}".format(len(self.devices)))

    def initialise(self):
        """Initialises BitLib library.
        
        Call to initialize the library. Optional unless dynamically loaded.
        """
        bitlib.BL_Initialize()

    def open(self, probe_files=None, count=1):
        """Opens Specified Number of Devices
        
        Open devices listed in probe file probe_files (string) or a literal list of links,
        also specified via probe_files (individual links are separated by newlines). If
        not specified, the standard probe file is used. Opens the first valid
        link found unless count is specified in which case count links are attempted and
        valid links are opened. Returns number of successfully opened links.

        :type probe_files: string or list of links
        :param probe_files: USB Port Connected to Bitscope
        :type count: int
        :param count: number of devices to be opened. default 1
        :returns: int opened device count
        """
        self.device_count = bitlib.BL_Open(probe_files, count)
        return self.device_count
    
    def halt(self):
        """Halt any prevailing streaming on the selected device.
        
        :returns: OK
        """
        return bitlib.BL_Halt()
    
    def count(self,type=bitlib.BL_COUNT_DEVICE):
        """Return the number of prevailing device available.
        
        :type type: int
        Available Options are
            COUNT.DEVICE - successfully opened devices
        
        :param type: specifies the type for which count must be found
        
        :return: count of the selected type
        """
        if type == bitlib.BL_COUNT_DEVICE:
            self.device_count = bitlib.BL_Count(type)
            return self.device_count
        else:
            logger.debug("Invalid Count Type")
            return 0

    def send(self,command,layer):
        """Send the command string S to the selected device on layer L (0=>scope,
        1=>generator). This function can be used with BL_Receive to send and
        receive command strings to a device effectively bypassing the library.

        :type command: string
        :param command: command to be sent to the signal scope or generator
        :type layer: int
        available options are
        LAYER.SCOPE - to send command to scope
        LAYER.GENERATOR - to send command to generator
        :param layer: selects the layer to which command is to be sent

        :returns: the same command sent
        """
        return bitlib.BL_Send(command,layer)        
    
    def version(self, type=bitlib.BL_VERSION_LIBRARY):
        """ Retruns version string of the selected type. 
        
        :type type: int
        :param type: Version type to display
        Available Options can be accessed as
    
        VERSION.DEVICE - device model and version identifier
        VERSION.LIBRARY - library version and production build ID
        VERSION.BINDING - language binding and version

        :returns: version string
        """
        if type in [bitlib.BL_VERSION_DEVICE, bitlib.BL_VERSION_LIBRARY, bitlib.BL_VERSION_BINDING]:
            return bitlib.BL_Version(type)
        else:
            logger.debug("Invaild Version Type Specified")

    def close(self):
        """Close all opened devices. Call this to release library resources and/or
        before opening (scope.open()) a new set of devices.
        """
        bitlib.BL_Close()

    def __del__(self):
        """Destroy the Scope Object.
        """
        logger.debug("Closing {} Bitscope Micro Units".format(len(self.devices)))
        bitlib.BL_Close()