"""Document level docstring."""
#!/usr/bin/env python

import bitlib 

from utils.logger import logger

class Channel:
    """channel class to select, configure and acquire data from channels."""
    
    id = None
    device = None
    src = None
    analog_count = None
    logic_count = None
    analog_range_count = None
    coupling = None

    def __init__(self, device, channel):
        """Initialise channel objects.
        
        :type device: int
        :param device: device id
        :type channel: int
        :param channel: channel id
        """
        self.device = device
        self.id = channel
        # device is seleted from previous Device class
        # select corresponding channel
        bitlib.BL_Select(bitlib.BL_SELECT_CHANNEL,channel)
        self.analog_count = bitlib.BL_Count(bitlib.BL_COUNT_ANALOG)
        self.logic_count = bitlib.BL_Count(bitlib.BL_COUNT_LOGIC)
        self.analog_range_count = bitlib.BL_Count(bitlib.BL_COUNT_RANGE)

    def select(self):
        """Request the selection of a current channel.
        
        :return: current selection of channel is returned.
        """
        # check if the corresponding device is already selected
        if self.device != bitlib.BL_Select(bitlib.BL_SELECT_DEVICE,bitlib.BL_ASK):
            # select the corresponding device first
            bitlib.BL_Select(bitlib.BL_SELECT_DEVICE,self.device)
        
        if self.id != bitlib.BL_Select(bitlib.BL_SELECT_CHANNEL,bitlib.BL_ASK):
            # select the corresponding channel next
            self.id = bitlib.BL_Select(bitlib.BL_SELECT_CHANNEL,self.id)
        
        return self.id
    
    def count(self,type):
        """Return the number of channels or ranges per the type specifier using the prevailing device and/or channel for those types that require it.
        
        :type type: int
        Available Options can be accessed as
            COUNT.ANALOG - analog channels on the selected device
            COUNT.LOGIC - logic channels on the selected device
            COUNT.RANGE - number of analog ranges on the selected channel
        
        :param type: specifies the type for which count must be found
        
        :return: count of the selected type
        """
        if type in [bitlib.BL_COUNT_ANALOG,bitlib.BL_COUNT_LOGIC,bitlib.BL_COUNT_RANGE]:
            if type == bitlib.BL_COUNT_ANALOG:
                self.analog_count = bitlib.BL_Count(type)
                return self.analog_count
            if type == bitlib.BL_COUNT_LOGIC:
                self.logic_count = bitlib.BL_Count(type)
                return self.logic_count
            if type == bitlib.BL_COUNT_RANGE:
                self.analog_range_count = bitlib.BL_Count(type)
                return self.analog_range_count
        else:
            logger.debug("Invalid Count Type")
            return 0
    
    def source(self,type=bitlib.BL_SOURCE_BNC):
        """Request the selection of a range or sources.
        
        :type type: int
        Available options are
            SOURCE.POD - analog or logic channel POD input
            SOURCE.BNC - analog channel BNC input (if available)
            SOURCE.X10 - analog input prescaled by 10
            SOURCE.X20 - analog input prescaled by 20
            SOURCE.X50 - analog input prescaled by 50
            SOURCE.ALT - alternate input (data acquisition)
            SOURCE.GND - ground reference input
        :param type: selects the type of source for a channel
        """
        self.select()
        
        if type in [bitlib.BL_SOURCE_POD, bitlib.BL_SOURCE_BNC, bitlib.BL_SOURCE_X10, bitlib.BL_SOURCE_X20, bitlib.BL_SOURCE_X50, bitlib.BL_SOURCE_ALT, bitlib.BL_SOURCE_GND]:
            if type != bitlib.BL_Select(bitlib.BL_SELECT_SOURCE,bitlib.BL_ASK):
                # select the corresponding source for the channel
                self.source = bitlib.BL_Select(bitlib.BL_SELECT_SOURCE,type)

        return self.source
    
    # set offset
    def offset(self, offset):
        """Request offset and return the offset that is actually assigned to to
        the selected device, channel and source. If a value beyond the
        available offset range of the device is specified the closest available
        offset for that channel is used.
        
        :type offset: int
        :param offset: the value to be offset
        
        :return: offset that is actually assigned to the selected device, channel and source.
        """
        self.select()
        # set offset
        return bitlib.BL_Offset(offset)
    
    # set range
    def analog_range(self, range):
        """Selects range and returns the maximum peak-to-peak voltage the can
        be captured on the selected device, channel and source. If the range is
        omitted, the prevailing range scale is returned. The range must
        otherwise be 0 to N where N is the number of available ranges).
        
        :type range: int
        :param range: maximum peak-to-peak voltage the can be captured on the selected device, channel and source.
        
        :return: returns the maximum peak-to-peak voltage
        """
        self.select()
        # set range
        if range >= 0 and range <= (self.analog_range_count)-1:
           return bitlib.BL_Range(range)
    
    # set coupling
    def coupling(self,coupling):
        """Selects coupling and returns the same value as A if the requested
        value is selectable on the current channel and source. If coupling is
        omitted (or bitlib.BL_ASK is specified), the prevailing coupling is returned.
        
        :type coupling: int
        Available options are
            COUPLING.DC - direct connection for DC signals (the default)
            COUPLING.AC - AC connection (eliminates DC bias)
            COUPLING.RF - RF connection for very high frequencies
        
        :param coupling: Selects coupling
        
        :return: the prevailing coupling is returned
        """
        self.select()
        if coupling in [bitlib.BL_COUPLING_AC,bitlib.BL_COUPLING_DC,bitlib.BL_COUPLING_RF,bitlib.BL_ASK]:
            
            return bitlib.BL_Coupling(coupling)
    
    def configure(self, source=bitlib.BL_SOURCE_BNC, offset=bitlib.BL_ZERO, range=0, coupling=bitlib.BL_COUPLING_DC):
        """Configure the channel parameters like source, offset, analog_range,
        coupling for the selected device and channel.
        
        :type source: 
        Available options are
            SOURCE.POD - analog or logic channel POD input
            SOURCE.BNC - analog channel BNC input (if available)
            SOURCE.X10 - analog input prescaled by 10
            SOURCE.X20 - analog input prescaled by 20
            SOURCE.X50 - analog input prescaled by 50
            SOURCE.ALT - alternate input (data acquisition)
            SOURCE.GND - ground reference input
        :param source: selects the type of source for a channel
        :type offset: int
        :param offset: the value to be offset
        :type range: int
        :param range: maximum peak-to-peak voltage the can be captured on the selected device, channel and source.
        :type coupling: int 
        Available options are
            COUPLING.DC - direct connection for DC signals (the default)
            COUPLING.AC - AC connection (eliminates DC bias)
            COUPLING.RF - RF connection for very high frequencies
        :param coupling: Selects coupling
        """

        self.select()
        if source in [bitlib.BL_SOURCE_POD, bitlib.BL_SOURCE_BNC, bitlib.BL_SOURCE_X10, bitlib.BL_SOURCE_X20, bitlib.BL_SOURCE_X50, bitlib.BL_SOURCE_ALT, bitlib.BL_SOURCE_GND]:
            # select the corresponding source for the channel
            bitlib.BL_Select(bitlib.BL_SELECT_SOURCE,source)
            self.source = source
            
        # set offset
        bitlib.BL_Offset(offset)
        # set range
        if range >= 0 and range <= (self.analog_range_count)-1:
            bitlib.BL_Range(range)
        # set coupling
        if coupling in [bitlib.BL_COUPLING_AC,bitlib.BL_COUPLING_DC,bitlib.BL_COUPLING_RF]:
            
            self.coupling = bitlib.BL_Coupling(coupling)
    
    # enable channel
    def enable(self):
        """Assign enable status E (boolean) on the selected channel.
        
        :return: True if successful or False otherwise.
        """
       
        self.select()
        logger.debug("Enabled Device : {} , Channel : {}".format(self.device,self.id))
        return bitlib.BL_Enable(1)
        
    
    # disable channel
    def disable(self):
        """Assign diasble status E (boolean) on the selected channel.
        
        :return: True if successful or False otherwise.
        """
        
        self.select()   
        logger.debug("Disabled Device : {} , Channel : {}".format(self.device,self.id))
        return bitlib.BL_Enable(0)
        
    
    # set index before reading the data 
    # assign the buffer offset (for dumps)
    def index(self, offset=0):
        """Request the capture address offset and return the address actually
        used A which may be different if the request is unavailable or invalid.
        If offset is omitted the address is (re)set to zero.
        
        :type offset: int
        :param offset: Request the capture address offset
        
        :return: the address actually used
        """
        
        self.select()
        return bitlib.BL_Index(offset)
    
    # acquire data from channel
    def acquire(self):
        """Reads N samples from the selected device (bitlib.BL_Select) and channel and
        writes them to list D.
        Returns N samples (possibly updated value). Samples are
        (nominally) floating point voltages. Logic channels are
        (nominally) low (0V) or high (5V). Alternatively D and/or N may
        be omitted. In either case the returned value is a new list of
        size N (or bitlib.BL_Size() if N is omitted).
        """
        
        self.select()
        logger.debug("Acquiring Data from Device : {} , Channel : {}".format(self.device,self.id))
        
        return bitlib.BL_Acquire()