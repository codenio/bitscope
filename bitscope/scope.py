from bitlib import *

class Scope:
    id = ""
    name = ""
    version = ""
    count = 0

    def __init__(self, count=1):
        print "Opening {} Bitscope Micro Units".format(count)
        BL_Open("",count)

        self.name = BL_Name()
        self.id = BL_ID()
        self.version = BL_Version()
        self.count = BL_Count()
        # variable to access functions inside class Select
        self.select = self.Select()

    class Select:
        def __init__(self):
            self.probes = self.Probe()

        # select device first
        def device(self,device):
            if type(device) is int:
                BL_Select(BL_SELECT_DEVICE,device)
            else:
                print "Invalid Device Number"
        
        # select mode
        def mode(self, mode):
            # select mode
            valid_modes = [BL_MODE_FAST,BL_MODE_DUAL,BL_MODE_MIXED,BL_MODE_LOGIC,BL_MODE_STREAM]
            if mode in valid_modes:
                BL_Mode(mode)
            else:
                print "Invalid Mode Specified"
        
        def channel(self, channel):
            # select channel
            if type(channel) is int:
                BL_Select(BL_SELECT_CHANNEL,channel)
            else:
                print "Invalid Channel Number"

        def probe(self,device, mode, channel):
            # select device
            if type(device) is int:
                BL_Select(BL_SELECT_DEVICE,device)
            else:
                print "Invalid Device Number"
            # select mode
            valid_modes = [BL_MODE_FAST,BL_MODE_DUAL,BL_MODE_MIXED,BL_MODE_LOGIC,BL_MODE_STREAM]
            if mode in valid_modes:
                BL_Mode(mode)
            else:
                print "Invalid Mode Specified"
            # select channel
            if type(channel) is int:
                BL_Select(BL_SELECT_CHANNEL,channel)
            else:
                print "Invalid Channel Number"
            print "selected device {}, mode {}, channel {}".format(device,mode,channel)
            return self.probes

        # probe is collective class representing the a channel 
        class Probe:
            def source(self,source=BL_SOURCE_BNC):
                # select source
                valid_sources = [BL_SOURCE_POD,BL_SOURCE_BNC,BL_SOURCE_X10,BL_SOURCE_X20,BL_SOURCE_X50,BL_SOURCE_ALT,BL_SOURCE_GND]
                if source in valid_sources:
                    BL_Select(BL_SELECT_SOURCE,source)            
                else:
                    print "Invalid Source Specified"

            def rate(self,rate=BL_MAX_RATE):
                BL_Rate(rate); # optional, default BL_MAX_RATE
            
            def size(self, size=BL_MAX_SIZE):
                BL_Size(size); # optional default BL_MAX_SIZE
            
            def pre_capture(self, pre_capture=BL_ZERO):
                BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
            
            def post_capture(self, post_capture=BL_ZERO):
                BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default

            def configure(self,source=BL_SOURCE_BNC, rate=BL_MAX_RATE, size=BL_MAX_SIZE, pre_capture=BL_ZERO, post_capture=BL_ZERO):
                # select source
                valid_sources = [BL_SOURCE_POD,BL_SOURCE_BNC,BL_SOURCE_X10,BL_SOURCE_X20,BL_SOURCE_X50,BL_SOURCE_ALT,BL_SOURCE_GND]
                if source in valid_sources:
                    BL_Select(BL_SELECT_SOURCE,source)            
                else:
                    print "Invalid Source Specified"
                #Setup channel-nonspecific parameters for capture.
                BL_Rate(rate); # optional, default BL_MAX_RATE
                BL_Size(size); # optional default BL_MAX_SIZE
                BL_Intro(pre_capture); #How many seconds to capture before the trigger event- 0 by default
                BL_Delay(post_capture); #How many seconds to capture after the trigger event- 0 by default
            
            def enable(self):
                BL_Enable(1)

    # def configure(self, range, offset, coupling)
    def __del__(self):
        print "Closing {} Bitscope Micro Units".format(self.count)
        BL_Close()