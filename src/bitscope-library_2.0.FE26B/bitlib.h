/* bitlib.h -- BitScope Library Version 2.0 FE26B (beta)
 *
 *     http://bitscope.com/software/library/guide/2.0/
 *
 * Copyright (C) 2015 BitScope Designs http://bitscope.com
 *
 * You may use this library software for any purpose, or distribute it
 * or derivative works in any form subject to the terms of the BitScope
 * Library Software Licence V1.1.
 */
#ifndef _BITLIB_H
#define _BITLIB_H

#if !defined(__cplusplus) 
#ifndef _bool_
#define _bool_
typedef unsigned int bool;
#endif
#ifndef TRUE
#define TRUE 1
#endif
#ifndef FALSE
#define FALSE 0
#endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

 /* magic values */

#define BL_MAX_RATE 0       /* request the maximum rate */
#define BL_MAX_TIME 0       /* request the maximum time */
#define BL_MAX_SIZE 0       /* request the maximum size */
#define BL_TRACE_FORCED 0   /* trace without (waiting for) trigger */ 
#define BL_TRACE_FOREVER -1 /* trace without timeout (possibly forever) */
#define BL_ZERO 0           /* zero volts (ground, reference, etc) */
#define BL_ASK -1           /* request a prevailing value */

 /* select/report tokens */

    enum { BL_COUNT_DEVICE, BL_COUNT_ANALOG, BL_COUNT_LOGIC, BL_COUNT_RANGE };
    enum { BL_SELECT_DEVICE, BL_SELECT_CHANNEL, BL_SELECT_SOURCE };
    enum { BL_STATE_IDLE, BL_STATE_ACTIVE, BL_STATE_DONE, BL_STATE_ERROR };
    enum { BL_SOURCE_POD, BL_SOURCE_BNC, BL_SOURCE_X10, BL_SOURCE_X20, BL_SOURCE_X50, BL_SOURCE_ALT, BL_SOURCE_GND };
	enum { BL_COUPLING_DC, BL_COUPLING_AC, BL_COUPLING_RF };
    enum { BL_MODE_FAST, BL_MODE_DUAL, BL_MODE_MIXED, BL_MODE_LOGIC, BL_MODE_STREAM };
	enum { BL_TRIG_RISE, BL_TRIG_FALL, BL_TRIG_HIGH, BL_TRIG_LOW, BL_TRIG_NONE };
    enum { BL_VERSION_DEVICE, BL_VERSION_LIBRARY, BL_VERSION_BINDING, BL_VERSION_PLATFORM, BL_VERSION_FRAMEWORK, BL_VERSION_NETWORK };
	enum { BL_SYNCHRONOUS, BL_ASYNCHRONOUS };

 /* Library API | Types */
    
    typedef int      ( BL_Acquire_t )         ( int, double * ); 
    typedef void     ( BL_Close_t )           ( void );
    typedef int      ( BL_Count_t )           ( int );
    typedef int      ( BL_Coupling_t )        ( int );
    typedef double   ( BL_Delay_t )           ( double ); 
    typedef bool     ( BL_Enable_t )          ( bool); 
    typedef int      ( BL_Error_t )           ( void );
    typedef bool     ( BL_Halt_t )            ( void );
    typedef char *   ( BL_ID_t )              ( void );
    typedef bool     ( BL_Index_t )           ( int );
    typedef void     ( BL_Initialize_t )      ( void );
    typedef double   ( BL_Intro_t )           ( double ); 
    typedef char *   ( BL_Log_t )             ( void );
    typedef int      ( BL_Mode_t )            ( int ); 
    typedef char *   ( BL_Name_t )            ( char * );
    typedef double   ( BL_Offset_t )          ( double );
    typedef int      ( BL_Open_t )            ( const char *, int );
    typedef double   ( BL_Range_t )           ( int );
    typedef bool     ( BL_Receive_t )         ( char *, int, int );
    typedef double   ( BL_Rate_t )            ( double );
    typedef int      ( BL_Select_t )          ( int, int );
    typedef void     ( BL_Send_t )            ( char *, int );
    typedef int      ( BL_Size_t )            ( int ); 
    typedef int      ( BL_State_t )           ( void ); 
    typedef double   ( BL_Time_t)             ( double );
    typedef bool     ( BL_Trace_t )           ( double, bool ); 
    typedef bool     ( BL_Trigger_t )         ( double, int );
    typedef char *   ( BL_Version_t )         ( int );
    
 /* Library API | Function Pointers */
    
    BL_Acquire_t BL_Acquire;
    BL_Close_t BL_Close;
    BL_Count_t BL_Count;
    BL_Coupling_t BL_Coupling;
    BL_Delay_t BL_Delay;
    BL_Enable_t BL_Enable;
    BL_Error_t BL_Error;
    BL_Halt_t BL_Halt;
    BL_ID_t BL_ID;
    BL_Initialize_t BL_Initialize;
    BL_Intro_t BL_Intro;
    BL_Log_t BL_Log;
    BL_Mode_t BL_Mode;
    BL_Name_t BL_Name;
    BL_Offset_t BL_Offset;
    BL_Open_t BL_Open;
    BL_Range_t BL_Range;
    BL_Rate_t BL_Rate;
    BL_Receive_t BL_Receive;
    BL_Select_t BL_Select;
    BL_Send_t BL_Send;
    BL_Index_t BL_Index;
    BL_Size_t BL_Size;
    BL_State_t BL_State;
    BL_Time_t BL_Time;
    BL_Trace_t BL_Trace;
    BL_Trigger_t BL_Trigger;
    BL_Version_t BL_Version;
        
#ifdef __cplusplus
}
#endif

#endif /* _BITLIB_H */
