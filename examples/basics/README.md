## Basics - Read Data

### Using Bitlib Library

```python
#!/usr/bin/env python

from bitlib import *

TRUE = 1
FALSE =0

#Setup general parameters for the capture
MY_RATE = 1000000 # default sample rate in Hz we'll use for capture.
MY_SIZE = 12288 # number of samples we'll capture - 12288 is the maximum size

print "Starting: Attempting to open one devices..."

#Attempt to open 1 device at /dev/ttyUSBx
#Make sure you run 'cd /dev/' followed by 'ls ' on terminal to see if the device is present.

#See return value to see the number of successfully opened devices.
if (BL_Open('USB:/dev/ttyUSB1',1)==0):
    print "  FAILED: all devices not found (check your probe file)."    
else:
    #Successfully opened one device
    #Report the number of devices opened, and the library version used
    print '\nNumber of devices opened: %s' %BL_Count(BL_COUNT_DEVICE)
    print " Library: %s (%s)\n\n" % (BL_Version(BL_VERSION_LIBRARY),BL_Version(BL_VERSION_BINDING))

    #Select the first device opened, found at location 0 by default.
    BL_Select(BL_SELECT_DEVICE,0)

    #Setup acquisition in FAST mode, where the whole of the 12288 samples in
    #the buffer are used by one channel alone.
    BL_Mode(BL_MODE_FAST)

    #Report the capture details
    print " Capture: %d @ %.0fHz = %fs" % (BL_Size(),BL_Rate(MY_RATE),BL_Time())

    #Setup channel-nonspecific parameters for capture.
    BL_Intro(BL_ZERO); #How many seconds to capture before the trigger event- 0 by default
    BL_Delay(BL_ZERO); #How many seconds to capture after the trigger event- 0 by default
    BL_Rate(MY_RATE); # optional, default BL_MAX_RATE
    BL_Size(MY_SIZE); # optional default BL_MAX_SIZE

    #Set up channel A properties - A has channel index 0, B has 1.
    #All the subsequent properties belong to channel A until another is selected.
    BL_Select(BL_SELECT_CHANNEL,0);

    #Setup a falling-edge trigger at 0.999V.
    #Other options are BL_TRIG_RISE, BL_TRIG_HIGH, BL_TRIG_LOW.
    BL_Trigger(0.999,BL_TRIG_FALL); # This is optional when untriggered BL_Trace() is used

    BL_Select(BL_SELECT_SOURCE,BL_SOURCE_POD); # use the POD input - the only one available
    BL_Range(BL_Count(BL_COUNT_RANGE)); # maximum range for y-axis - use this whenever possible
    BL_Offset(BL_ZERO); # Y-axis offset is set to zero as BL_ZERO

    #Enable the currently selected channel, i.e. channel A
    #This ensures the recorded data goes into the memory-buffer in Bitscope device
    BL_Enable(TRUE);

    print " Bitscope Enabled"

    #Capture analog data synchronously to the Bitscope device's buffer.
    #If a trigger event is not received in 0.1sec, auto trigger happens.
    #BL_Trace(), when without any arguments, captures immediately, no trigger needed.
    print "trace {}".format(BL_Trace(0.01, BL_SYNCHRONOUS))

    #Transfer the captured data to our PC's memory using the USB link
    DATA = BL_Acquire()

    print DATA

    # Close the library to release resources (we're done).
    BL_Close()

    print "Finished: Library closed, resources released."

```


### Using Bitscope Library

```python
#!/usr/bin/env python

from bitscope import *

#Setup general parameters for the capture
MY_RATE = 1000000 # default sample rate in Hz we'll use for capture.
MY_SIZE = 12288 # number of samples we'll capture - 12288 is the maximum size

print "Starting: Attempting to open one devices..."

#Attempt to open 1 device at /dev/ttyUSBx
#Make sure you run 'cd /dev/' followed by 'ls ' on terminal to see if the device is present.

# initialisation of scope collects all the device data and stores them in scope.devices list
# and closes open devices on object termination 
scope = Scope('USB:/dev/ttyUSB1',1)

#See return value to see the number of successfully opened devices.
if (scope.device_count==0):
    print "  FAILED: all devices not found (check your probe file)."    
else:
    #Successfully opened one device
    #Report the number of devices opened, and the library version used
    print '\nNumber of devices opened: %s' %scope.device_count
    print " Library: %s (%s)\n\n" % (scope.version(VERSION.LIBRARY),scope.version(VERSION.BINDING))

    # collect the list of devices
    devices = scope.devices

    #Select the first device opened, found at location 0 by default.
    #Setup acquisition in FAST mode, where the whole of the 12288 samples in
    #the buffer are used by one channel alone.
    devices[0].mode(MODE.FAST)
    
    #Report the capture details
    print " Capture: %d @ %.0fHz = %fs" % (scope.tracer.size(),scope.tracer.rate(MY_RATE),scope.tracer.time())

    #Setup channel-nonspecific parameters for capture.
    scope.tracer.configure(
        rate=MY_RATE, # optional, default BL_MAX_RATE
        size=MY_SIZE, # optional default BL_MAX_SIZE
        pre_capture=ZERO, #How many seconds to capture before the trigger event- 0 by default
        post_capture=ZERO, #How many seconds to capture after the trigger event- 0 by default
    )

    #Set up channel A properties - A has channel index 0, B has 1.
    #All the subsequent properties belong to channel A until another is selected.
    
    #Setup a falling-edge trigger at 0.999V.
    #Other options are BL_TRIG_RISE, BL_TRIG_HIGH, BL_TRIG_LOW.
    scope.tracer.trigger(0.999,TRIGGER.FALL)

    # select channel 0 form device 0 and configure 
    devices[0].channels[0].configure(
        source=SOURCE.POD, # use the POD input - the only one available
        offset=ZERO, # Y-axis offset is set to zero as BL_ZERO
        range=devices[0].channels[0].analog_range_count, # maximum range for y-axis - use this whenever possible
        coupling=COUPLING.AC
    )
    
    #Enable the currently selected channel, i.e. channel A
    #This ensures the recorded data goes into the memory-buffer in Bitscope device
    devices[0].channels[0].enable()
    
    #Capture analog data synchronously to the Bitscope device's buffer.
    #If a trigger event is not received in 0.1sec, auto trigger happens.
    #BL_Trace(), when without any arguments, captures immediately, no trigger needed.
    print "trace {}".format(scope.tracer.trace(0.01,TRACE.SYNCHRONOUS))

    #Transfer the captured data to our PC's memory using the USB link
    DATA = devices[0].channels[1].acquire()
    
    print DATA

    print "Finished: Library closed, resources released."
```

