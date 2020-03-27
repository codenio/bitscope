# Design Docs

## scope
    BL_Initialize - initialize the library (optional)
    BL_Open - open one or more devices
    BL_Halt - all any pending or prevailing device activity
    BL_Close - close all open devices
    BL_Version - return the version of the library (BL_VERSION_LIBRARY)

## device
    BL_Select - select a device, channel or source (BL_SELECT_DEVICE)
    BL_ID - return the selected device ID
    BL_Name - return the device link name 
    BL_Count - count devices, channels, or ranges (BL_COUNT_CHANNEL)
    BL_Version - return the version (BL_VERSION_DEVICE)
    BL_Mode - select and trace mode    

## channel
    BL_Select - select a device, channel or source (BL_SELECT_CHANNEL)
    BL_Select - select a device, channel or source (BL_SELECT_SOURCE)
    BL_Count - count devices, channels, or ranges (BL_COUNT_RANGE)
    BL_Offset - assign channel offset
    BL_Range - select the channel range
    BL_Coupling - select the channel source coupling
    BL_Enable - change channel enable status

## trace
    BL_Rate - assign the sample rate
    BL_Size - assign the capture size (samples)
    BL_Time - assign the capture duration (seconds)
    BL_Trigger - set up the trigger
    BL_Intro - assign the pre-trigger size (intro region)
    BL_Delay - assign post-trigger delay

## capture
    BL_State - return capture engine state
    BL_Index - assign the buffer offset (for dumps)
    BL_Trace - initiate capture
    BL_Acquire - dump data from the device

## utils
    BL_Log - dump the pending log
    BL_Error - return most recent error (if any)