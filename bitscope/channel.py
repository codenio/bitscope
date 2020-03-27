"""Document level docstring."""
#!/usr/bin/env python

from bitlib import *

class Channel:
    """channel class to select, configure and acquire data from channels."""
    
    id = None
    device = None
    src = None
    analog_count = None
    logic_count = None
    analog_range_count = None

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
        BL_Select(BL_SELECT_CHANNEL,channel)
        self.analog_count = BL_Count(BL_COUNT_ANALOG)
        self.logic_count = BL_Count(BL_COUNT_LOGIC)
        self.analog_range_count = BL_Count(BL_COUNT_RANGE)

    def select(self):
        """Request the selection of a current channel.
        
        :return: current selection of channel is returned.
        """
        # check if the corresponding device is already selected
        if self.device != BL_Select(BL_SELECT_DEVICE,BL_ASK):
            # select the corresponding device first
            BL_Select(BL_SELECT_DEVICE,self.device)
        
        if self.id != BL_Select(BL_SELECT_CHANNEL,BL_ASK):
            # select the corresponding channel next
            BL_Select(BL_SELECT_CHANNEL,self.id)
        
        # print "Selected Device : {} , Channel : {}".format(self.device,self.id)
    
    def count(self,type):
        """Return the number of channels or ranges per the type specifier(BL_COUNT_ANALOG=>devices, BL_COUNT_LOGIC=>analog, 2=>logic, BL_COUNT_RANGE=>ranges) using the prevailing device and/or channel for those types that require it.
        
        :type type: BL_COUNT_ANALOG,BL_COUNT_LOGIC,BL_COUNT_RANGE
        :param type: specifies the type for which count must be found
        :return: count of the selected type
        """
        if type in [BL_COUNT_ANALOG,BL_COUNT_LOGIC,BL_COUNT_RANGE]:
            return BL_Count(type)
        else:
            print "Invalid Count Type"
            return 0
    
    def source(self,type=BL_SOURCE_BNC):
        """Request the selection of a range or sources.
        
        :type type: BL_SOURCE_POD, BL_SOURCE_BNC, BL_SOURCE_X10, BL_SOURCE_X20, BL_SOURCE_X50, BL_SOURCE_ALT, BL_SOURCE_GND
        :param type: selects the type of source for a channel
        """
        self.select()
        
        if type in [BL_SOURCE_POD, BL_SOURCE_BNC, BL_SOURCE_X10, BL_SOURCE_X20, BL_SOURCE_X50, BL_SOURCE_ALT, BL_SOURCE_GND]:
            # select the corresponding source for the channel
            BL_Select(BL_SELECT_SOURCE,type)
            self.source = type
    
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
        BL_Offset(offset)
    
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
            BL_Range(range)
    
    # set coupling
    def coupling(self,coupling):
        """Selects coupling and returns the same value as A if the requested
        value is selectable on the current channel and source. If coupling is
        omitted (or BL_ASK is specified), the prevailing coupling is returned.
        
        :type coupling: BL_COUPLING_AC,BL_COUPLING_DC,BL_COUPLING_RF,BL_ASK
        :param coupling: Selects coupling
        :return: the prevailing coupling is returned
        """
        self.select()
        if coupling in [BL_COUPLING_AC,BL_COUPLING_DC,BL_COUPLING_RF,BL_ASK]:
            return BL_Coupling(coupling)
    
    def configure(self, source=BL_SOURCE_BNC, offset=BL_ZERO, range=0, coupling=BL_COUPLING_DC):
        """Configure the channel parameters like source, offset, analog_range,
        coupling for the selected device and channel.
        
        :type source: BL_SOURCE_POD, BL_SOURCE_BNC, BL_SOURCE_X10, BL_SOURCE_X20, BL_SOURCE_X50, BL_SOURCE_ALT, BL_SOURCE_GND
        :param source: selects the type of source for a channel
        :type offset: int
        :param offset: the value to be offset
        :type range: int
        :param range: maximum peak-to-peak voltage the can be captured on the selected device, channel and source.
        :type coupling: BL_COUPLING_AC,BL_COUPLING_DC,BL_COUPLING_RF,BL_ASK
        :param coupling: Selects coupling
        """

        self.select()
        if source in [BL_SOURCE_POD, BL_SOURCE_BNC, BL_SOURCE_X10, BL_SOURCE_X20, BL_SOURCE_X50, BL_SOURCE_ALT, BL_SOURCE_GND]:
            # select the corresponding source for the channel
            BL_Select(BL_SELECT_SOURCE,source)
            self.source = source
            
        # set offset
        BL_Offset(offset)
        # set range
        if range >= 0 and range <= (self.analog_range_count)-1:
            BL_Range(range)
        # set coupling
        if coupling in [BL_COUPLING_AC,BL_COUPLING_DC,BL_COUPLING_RF]:
            BL_Coupling(coupling)
    
    # enable channel
    def enable(self):
        """Assign enable status E (boolean) on the selected channel.
        
        :return: true if successful or false otherwise.
        """
        self.select()
        BL_Enable(1)
        print "Enabled Device : {} , Channel : {}".format(self.device,self.id)
    
    # disable channel
    def disable(self):
        """Assign diasble status E (boolean) on the selected channel.
        
        :return: true if successful or false otherwise.
        """
        self.select()   
        BL_Enable(0)
        print "Disabled Device : {} , Channel : {}".format(self.device,self.id)
    
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
        return BL_Index(offset)
    
    # acquire data from channel
    def acquire(self):
        """Reads N samples from the selected device (BL_Select) and channel and
        writes them to list D.
        Returns N samples (possibly updated value). Samples are
        (nominally) floating point voltages. Logic channels are
        (nominally) low (0V) or high (5V). Alternatively D and/or N may
        be omitted. In either case the returned value is a new list of
        size N (or BL_Size() if N is omitted).
        """
        self.select()
        print "Acquiring Data from Device : {} , Channel : {}".format(self.device,self.id)
        return BL_Acquire()