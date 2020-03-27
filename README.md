[![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/downloads/release/python-2715/)  [![PyPI version](https://badge.fury.io/py/bitscope.svg)](https://badge.fury.io/py/bitscope) [![bitlib version](https://img.shields.io/badge/bitlib-2.0-blue)](http://bitscope.com/software/library/guide/2.0/#blindex-assign-the-buffer-offset-for-dumps)  [![GitHub license](https://img.shields.io/github/license/codenio/bitscope)](https://github.com/codenio/bitscope/blob/master/LICENSE)

# bitscope

**bitscope** is a comprehensive library for programming and data collection from Bitscope Micro.

It is a python wrapper for **bitlib** package installed using **bitscope-library_2.0.FE26B** and **python-bindings-2.0-DC01L**


## Install

- clone this repository using
    ```bash
    $ git clone git@github.com:codenio/bitscope.git
    ```
- install `bitlib` library from ./src directory
    
    ```bash
    # cd into bitscope/src/ directory
    $ cd bitscope/src/
    
    # install the bitscope-library_2.0 debian package
    $ sudo apt-get install bitscope-library_2.0.FE26B_amd64.deb
    
    # unzip and cd into bitscope/src/python-bindings-2.0-DC01L/ 
    $ unzip python-bindings-2.0-DC01L.zip
    $ cd python-bindings-2.0-DC01L/
    
    # install bitlib using the python-binding script 
    $ sudo python setup-bitlib.py install
    
    # in case of errors.. try
    $ sudo BASECFLAGS="" OPT="" CFLAGS="-O3" python setup-bitlib.py install
    ```

    Note: the files, debian packages and steps to install were taking from [murgen-dev-kit](https://github.com/kelu124/murgen-dev-kit/tree/master/software). thanks to [K.Ghosh](https://github.com/kelu124)

- to install stable version of **bitscope** package
    ```bash
    $ sudo pip install bitscope
    ```
- connect your bitscope to your pc and test the functionality using
the example file at `bitscope/examples/scope/scope_plot.py`
    ```bash
    $ python ./examples/scope/scope_plot.py
    ```

## Library Overview

The Library provides full programmed access to the BitScope Capture Engine. It is implemented using a small set of portable functions. Programming BitScope to capture waveforms and logic is simply a matter of calling the correct sequence of these functions from your program.

See BitScope Programming and Library Reference for details.

### BitScope Programming
Regardless of the device and library functions used, BitScope programming always follows a familiar sequence:

```php
(1) Initialize -> (2) Setup -> (3) Trace -> (4) Acquire -> (5) Close
```

The library must first be **(1) initialized** and one or more devices opened. For each open device the required capture conditions must be **(2) set up** before a **(3) trace** is initiated to capture or generate the signals. When the trace completes the data may be **(4) acquired** to the host computer for display and analysis. Initialization and setup is normally only done once but the trace and acquire steps may be repeated as often as required. When finished the devices should be **(5) closed** which releases the resources allocated to them.

#### (1) Library and Device Initialization
Before use, the library must be initialized and one or more devices opened:

```python
# initialize the library and open one or more devices
>>> from  bitscope import *
# The call Scope() is implicit (in most cases); calling Scope() to open the device(s) is sufficient to initialize the library.
>>> scope = Scope("USB:/dev/ttyUSB0",1)
Bitscope Micro Units Opened : 1
```


When the device is open, information about it may be obtained:

```python
# count open devices
>>> len(scope.devices)
1

# scope.devices is a list that contains device objects for the currently open devices 
>>> type(scope.devices)
<type 'list'>

# assign a specific device to a variable and use them conviniently
>>> deviceA = scope.devices[0]

# return the device link name
>>> deviceA.name
'USB:/dev/ttyUSB0'
# or 
>>> scope.devices[0].name
'USB:/dev/ttyUSB0'

# return version information
>>> deviceA.version
'BS000501'

# return the selected device ID
>>> deviceA.id
0 
```

these functions are necessary only for reporting information to the application and identifying the device.

#### (2) Device Programming and Setup

After one or more devices have been opened they must be set up for use. This is the most detailed programming step but it is only needed once after opening the device unless recovering from an error. The first thing your program needs to know is how many devices, channels, ranges and other properties are available (they may not all be the same). The number of open devices may be obtained via `len(scope.devices)`.

```python
# each devices conatins a list of channels objects avaialable in them
>>> type(scope.devices[0].channels)
<type 'list'>

# assign a specific chanel to a variable and use them conviniently
>>> ch_0 = scope.devices[0].channels[0] 

# count analog and logic channels, or ranges
# supported types: BL_COUNT_ANALOG,BL_COUNT_LOGIC,BL_COUNT_RANGE
# scope.devices[0].channels[0].count(type)
>>> scope.devices[0].channels[0].count(BL_COUNT_ANALOG)
2
# or
>>> ch_0.count(BL_COUNT_ANALOG)
2
>>> ch_0.count(BL_COUNT_LOGIC)
8
>>> ch_0.count(BL_COUNT_RANGE)
1
```

`channel.Count(type)` method is used to report the number of analog channels, logic channels and analog input ranges (on each analog channel). Which entity it reports depends on its argument and which device, channel or source is selected a the time it is called. The device, channel and source are selected using `.select()` method:

```python
# select a device
>>> scope.devices[0].select()

# select a channel of a particular device
# selection of channel is implicit, it selects the corresponding device first if it is not selected.
>>> scope.devices[0].channel[0].select()
```

When the device is selected for the first time, its trace mode must also be selected:

```python
# select a trace mode
# supported mode type : BL_MODE_FAST, BL_MODE_DUAL, BL_MODE_MIXED, BL_MODE_LOGIC, BL_MODE_STREAM
# scope.devices[0].mode(type) -  it selects the device implicitly and then sets the mode for the device
>>> scope.devices[0].mode(BL_MODE_DUAL)
Device : 0 set to Mode : 1
```

Note : It must be called after selecting the device(selected implicitly) but before selecting the channel. This is important because the number of channels available may be fewer than the physical number the device supports in some modes.

**For example**, to select the BNC source on channel 1 on device 0:
```python
# scope.devices[0].select() - implicitly selected during mode set
scope.devices[0].mode(BL_MODE_FAST);
scope.devices[0].channels[0].source(BL_MODE_FAST);
```

Once the device and mode are selected, each channel may be selected in turn and configured to choose a source, input offset, voltage range, signal coupling and whether to enable it for capture:

```python
# assign a specific chanel to a variable and use them conviniently
>>> ch_0 = scope.devices[0].channels[0]
# select the channel range
>>> ch_0.range()
#assign channel offset
>>> ch_0.gffset()
#select the channel source coupling
>>> ch_0.coupling()
#change channel enable status
>>> ch_0.enable()

# or use configure to configure it at ones
>>> ch_0.configure(
            source=BL_SOURCE_POD,
            offset=BL_ZERO,
            analog_range=BL_Count(BL_COUNT_RANGE),
            coupling=BL_COUPLING_DC
        )

# enable the channel to capture the data from specific channel - selects the channel implicitly
>>> scope.devices[0].channels[0].enable()
Enabled Device : 0 , Channel : 0
# or 
>>> ch_0.enable()
Enabled Device : 0 , Channel : 0
```

For each channel enabled for capture, this process is repeated as required. When the channels are all configured, the trace may be programmed.

#### (3) Trace Programming and Capture
After the device, mode and channels are configured, trace settings are programmed. First the sample rate and capture size (specified in samples) are assigned:

```python
# assign the sample rate (Hz)
>>> scope.tracer.rate()
20000000.0
# assign the capture size (samples)
>>> scope.tracer.size()
12288
```

This must be done first to establish the core trace settings. Choose values to ensure the duration required will be captured given the selected sample rate. Some modes use finite (device) buffers so your choice may be constrained. An alternative is to assign the duration directly:

```python
# assign the capture duration (seconds)
>>> scope.tracer.time()
0.0006144
```
In this case, the capture size and sample rate may be adjusted by the library automatically. Next the trigger, if required, is established:

```python
# set up the trigger
# supported types : BL_TRIG_RISE, BL_TRIG_FALL, BL_TRIG_HIGH, BL_TRIG_LOW, BL_TRIG_NONE
>>> scope.tracer.trigger(volt=0.999, kind=BL_TRIG_FALL)
```

This function accepts two arguments specifying the trigger level (which is applied to the currently selected channel) and the type of trigger. If signals are to be captured before the trigger, or a delay is required after the trigger, these parameters are specified next using two functions:

```python
# assign the pre-trigger size (intro region)
# default : BL_ZERO
>>> scope.tracer.pre_captutre(t=BL_ZERO)

# assign post-trigger delay (delay before capture)
# default : BL_ZERO
>>> scope.tracer.post_captutre(t=BL_ZERO)
```

Both functions are optional (not required when tracing untriggered). At this point the device is ready to capture waveforms and logic data. All the preceding steps need not be repeated if the parameters for a series of captures remain unchanged. To commence the trace and capture signals call:

```python
# initiate capture
# supported types : BL_SYNCHRONOUS,BL_ASYNCHRONOUS
>>> scope.tracer.trace(time_out=0.01, sync=BL_SYNCHRONOUS)
```

This function is the one that actually talks to BitScope and captures waveforms. This function may take an arbitrarily long time to complete. Indeed it may never complete, so to avoid locking your program, it may be called asynchronously or it may be called with a specified timeout. When called asynchronously `scope.tracer.trace()` always returns immediately, even if the trace has not yet completed. In this case call:

```python
# return capture engine state
>>> scope.tracer.state()
```

periodically after `scope.tracer.trace()` to monitor progress of the trace. `scope.tracer.state()` returns a token reporting trace in progress, trace complete, timeout or an error code. When an asynchronous trace is in progress it may be manually stopped with:

```python
# all any pending or prevailing device activity
>>> scope.halt()
```
An alternative is to call `scope.tracer.state()` synchronously with a specified timeout. In this case `scope.tracer.state()` is guaranteed to return within the time specified but the trace may or may not have completed in that time; it returns TRUE if it has, FALSE otherwise.

#### (4) Acquiring Data from the Device
Once the trace has completed, the data may be acquired:

```python
# acquire data from the device and channel specifically - both device and channel is implictly selected
>>> DATA = scope.devices[0].channels[0].acquire()
# or
>>> DATA = ch_0.acquire()
```

`ch_0.acquire()` uploads data from the device one channel at a time. Before it is called each time, select the channel (and optionally the device) to be acquired with BL_Select. If acquiring from other than the first sample, the starting index may be specified:

```python
# assign the buffer offset (for acquisition)
>>> scope.devices[0].channels[0].index(offset=100)
```

If `channel.index()` is used it must be called before `scope.tracer.trace()`. In any case, the return value of `channel.acquire()` specifies how many sample are actually acquired. The return value will not be greater than the number requested but it may be fewer:

If the number of samples captured is fewer than the number requested,
If the trace was terminated early, a timeout or error occured, or
A programming error (such as forgetting to enable the channel).
Typically one executes `scope.tracer.trace()` and cycles through a sequence of `channel.acquire()`, one for each channel (on each device), before executing the next `scope.tracer.trace()`.

#### (5) Closing Devices and the Library
When you’re finished with the library, call `scope.close()`. This closes all open devices (it’s not possible to close only one). If you wish to close one of several devices, close them all and reopen those you wish to continue using.

## Develope

- make the suitable changes and from the root directory of this repository, install the bitscope python package using the install.sh script
    ```bash
    $ sudo ./scripts/install.sh
    ``` 

## Contribute

- You've discovered a bug or something else you want to change - excellent! - feel free to raise a issue.
- You've worked out a way to fix it – even better! - submit your PR
- You want to tell us about it – best of all!

Start contributing !