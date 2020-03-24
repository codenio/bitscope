/* bitlib -- BitScope Python Library API Bindings V2.0.
 *
 * http://www.bitscope.com/software/library/API.html
 *
 * Copyright (C) 2012, 2013 BitScope Designs http://bitscope.com
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, http://www.gnu.org/licenses/.
 *
 * Note#1 some API calls have been modified (compared with 1.4). 
 * See bitlib.h for details of these (minor) changes.
 *
 * Note#2 some functions are depreciated and are not implemented
 * in these Python bindings. If you don't know what they are you
 * won't miss them. If you do miss them you can add them yourself
 * as the library still implement them.
 *
 * Somewhat non-standard code formatting conventions are used here.
 * Fontification makes it easier to read (if you really want to) */

#include <Python.h> /* python extension library */
#include <bitlib.h> /* bitscope library api */

#define BL_PYTHON_VERSION "Python DC01L";

static char bitlib_doc[] = "BitScope Library API 2.0.\n\n\
The Python Bindings provided by this module replicate their C function\n\
counterparts. Refer to the BitLib C API reference for details:\n\n\
    http://bitscope.com/software/library/API.html\n\n\
BitLib is a programming library for all current model BitScopes.\n\n\
It abstracts the BitScope Virtual Machine into a functional API that\n\
supports connecting to BitScope, setting up trigger conditions,\n\
performing a waveform capture and acquiring captured data as well as\n\
more specialized functions such as generating signals and capturing\n\
continuous waveforms.\n\n\
BitScopes capture signals in various modes (see BL_Mode) but all modes\n\
are programmed in a similar multi-phase manner:\n\n\
    Open -> Setup -> Trace -> Acquire -> Close\n\n\
Initialise using BL_Open (BL_Initialize is optional).\n\n\
Setup is the most detailed phase and uses a selection of BL_Select\n\
BL_Mode, BL_Offset, BL_Enable, BL_Rate,\n\
BL_Time, BL_Size BL_Intro and BL_Trigger.\n\n\
Trace performs the actual data capture via BL_Trace.\n\n\
Acquire reads the captured data from the device channel by channel and\n\
uses BL_SelectChannel, BL_Index and BL_Acquire.";

static char bitlib_BL_Acquire_doc[] = "BL_Acquire(N, D) -> N\nBL_Acquire(N) -> D\nBL_Acquire() -> D\n\n\
Reads N samples from the selected device (BL_Select) and\n\
channel and writes them to list D. Returns N\n\
samples (possibly updated value). Samples are (nominally) floating\n\
point voltages. Logic channels are (nominally) low (0V) or high (5V).\n\
Alternatively D and/or N may be omitted. In either case the returned\n\
value is a new list of size N (or BL_Size() if N is omitted).";
static PyObject * bitlib_BL_Acquire ( PyObject * self, PyObject * args ) {
	PyObject * L = NULL; int N = 0; bool Alternate = 0;
	if ( ! PyArg_ParseTuple(args, "|iO", &N, &L) )
		return NULL;
	if ( N <= 0 )
		N = BL_Size(BL_ASK);
	if ( N <= 0 ) {
		PyErr_SetString(PyExc_TypeError, "Acquisition size is unknown."); 
		return NULL;
	}
	if ( L && ! PyList_Check( L ) ) {
		PyErr_SetString(PyExc_TypeError, "Second argument should be a list."); 
		return NULL;
	} else { int i; double D[N];
		N = BL_Acquire( N, D );
		if ( N > 0 ) {
			if ( ! L ) {
				L = PyList_New(N);
				Alternate = 1;
			}
			for ( i = 0; i < N; i++ ) 
				PyList_SetItem( L, i, PyFloat_FromDouble( D[i]) );
			if ( Alternate ) 
				return L;
		}
		return PyInt_FromLong( (long) N );
	}
}

static char bitlib_BL_Size_doc[] = "BL_Size(S) -> N\n\n\
Returns N, the number of samples to be captured (per frame) at the\n\
prevailing sample rate (BL_Rate) and duration (BL_Time)\n\
if S = 0. Returns the largest available buffer if S = -1. Returns\n\
the specified size S (if physicall possible) otherwise.";
static PyObject * bitlib_BL_Size ( PyObject * self, PyObject * args ) {
	int size = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|i:BL_Size", &size) ) return NULL;
	return PyInt_FromLong( (long) BL_Size(size) );
}

static char bitlib_BL_Time_doc[] = "BL_Time(R) -> A\n\n\
Request a capture duration R (in seconds) and return duration A that\n\
will actually be used. They are usually the same but may differ if the\n\
available buffer (BL_Size) is insufficient for the assigned sample\n\
rate (BL_Rate). If R = 0 (or omitted) the prevailing duration is\n\
returned without change.";
static PyObject * bitlib_BL_Time ( PyObject * self, PyObject * args ) {
	double time = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|d:BL_Time", &time) ) return NULL;
	return PyFloat_FromDouble( BL_Time(time) );
}

static char bitlib_BL_Enable_doc[] = "BL_Enable(E) -> OK\n\n\
Assign enable status E (boolean) on the selected channel. Return OK\n\
true if successful or false otherwise.";
static PyObject * bitlib_BL_Enable ( PyObject * self, PyObject * args ) {
	bool enable;
	if ( !PyArg_ParseTuple(args, "b:BL_Enable", &enable) ) return NULL;
	if ( BL_Enable(enable) ) Py_RETURN_TRUE; else Py_RETURN_FALSE;
}

static char bitlib_BL_Close_doc[] = "BL_Close()\n\n\
Close all opened devices. Call this to release library resources and/or\n\
before opening (BL_Open) a new set of devices.";
static PyObject * bitlib_BL_Close ( PyObject * self, PyObject * args ) {
    BL_Close();
	Py_RETURN_TRUE;
}

static char bitlib_BL_Count_doc[] = "BL_Count(T) -> N\n\n\
Returns the number of devices, channels or ranges per the type\n\
specifier (0=>devices, 1=>analog, 2=>logic, 3=>ranges) using the\n\
prevailing device and/or channel for those types that require it.";
static PyObject * bitlib_BL_Count ( PyObject * self, PyObject * args ) {
    int target = BL_COUNT_DEVICE;
	if ( !PyArg_ParseTuple(args, "|i:BL_Count", &target) ) return NULL;
	return PyInt_FromLong( (long) BL_Count(target) );
}

static char bitlib_BL_Coupling_doc[] = "BL_Coupling(R) -> A\n\n\
Selects coupling R and returns the same value as A if the requested\n\
value is selectable on the current channel and source (BL_Select). If\n\
coupling is omitted (or BL_ASK is specified), the prevailing coupling\n\
is returned.";
static PyObject * bitlib_BL_Coupling ( PyObject * self, PyObject * args ) {
    int coupling = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|i:BL_Coupling", &coupling) ) return NULL;
	return PyInt_FromLong( (long) BL_Coupling(coupling) );
}

static char bitlib_BL_State_doc[] = "BL_State() -> S\n\n\
Return (asynchronous) state S (0=>idle, 1=>armed, 2=>captured, 3=>timeout)\n\
Valid after BL_Trace is called asynchronously (viz).";
static PyObject * bitlib_BL_State
 ( PyObject * self, PyObject * args ) {
	return PyInt_FromLong( (int)BL_State() );
}

static char bitlib_BL_Halt_doc[] = "BL_Halt() -> OK\n\n\
Halt any prevailing streaming on the selected device.";
static PyObject * bitlib_BL_Halt ( PyObject * self, PyObject * args ) {
	if ( BL_Halt() ) Py_RETURN_TRUE;  else Py_RETURN_FALSE;
}

static char bitlib_BL_ID_doc[] = "BL_ID() -> ID\n\n\
Return unique identifier ID (string) of the selected (BL_Select) device.";
static PyObject * bitlib_BL_ID ( PyObject * self, PyObject * args ) {
	return PyString_FromFormat( BL_ID() );
}

static char bitlib_BL_Initialize_doc[] = "Initializes API.\n\n\
Call to initialize the library. Optional unless dynamically loaded.";
static PyObject * bitlib_BL_Initialize ( PyObject * self, PyObject * args ) {
    BL_Initialize();
	Py_RETURN_TRUE;
}

static char bitlib_BL_Log_doc[] = "BL_Log() -> Log\n\n\
Dump (and then erase) the accumulated library activity log. This is diagnostic aid.";
static PyObject * bitlib_BL_Log ( PyObject * self, PyObject * args ) {
	return PyString_FromFormat( BL_Log() );
}

static char bitlib_BL_Mode_doc[] = "BL_Mode(M) -> M\n\n\
Assign mode M (0=>SCOPE, 1=>CHOP, 2=>MIXED, 3=>LOGIC, 4=>STREAM)\n\
to the selected device (BL_Select) and return the mode if successful.";
static PyObject * bitlib_BL_Mode ( PyObject * self, PyObject * args ) {
	int mode = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|i:BL_Mode", &mode) ) return NULL;
    return PyInt_FromLong( (long) BL_Mode(mode) );
}

static char bitlib_BL_Name_doc[] = "BL_Name() -> N\n\n\
Returns the connection name N (string) for the selected device.";
static PyObject * bitlib_BL_Name ( PyObject * self, PyObject * args ) {
    char array[100];
	return PyString_FromFormat( BL_Name(array) );
}

static char bitlib_BL_Open_doc[] = "BL_Open(P, R) -> A\n\n\
Open devices listed in probe file P (string) or a literal list of links,\n\
also specified via P (individual links are separated by newlines). If\n\
not specified, the standard probe file is used. Opens the first valid\n\
link found unless R is specified in which case R links are attempted and\n\
valid links are opened. Returns A successfully opened links.";
static PyObject * bitlib_BL_Open ( PyObject * self, PyObject * args ) {
    char * probe = "bitscope.prb"; int count = 1;
	if ( !PyArg_ParseTuple(args, "|si:BL_Open", &probe, &count) ) return NULL;
	return PyInt_FromLong( (long) BL_Open( probe, count ) );
}

static char bitlib_BL_Intro_doc[] = "BL_Intro(R) -> A\n\n\
Request pretrigger hold-off duration D (in seconds) and return duration\n\
A that will actually be used. They are usually the same but may differ\n\
depending on the capabilities of the connected device.";
static PyObject * bitlib_BL_Intro ( PyObject * self, PyObject * args ) {
	double time;
	if ( !PyArg_ParseTuple(args, "d:BL_Intro", &time)) return NULL;
	return PyFloat_FromDouble( BL_Intro(time) );
}

static char bitlib_BL_Range_doc[] = "BL_Range(R) -> V\n\n\
Selects range R and returns the maximum peak-to-peak voltage the can be\n\
captured on the selected device, channel and source (BL_Select). If the\n\
range is omitted, the prevailing range scale is returned. The range\n\
must otherwise be 0 to N where N is the number of available ranges).";
static PyObject * bitlib_BL_Range ( PyObject * self, PyObject * args ) {
    int range = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|i:BL_Range", &range) ) return NULL;
    return PyFloat_FromDouble( BL_Range(range) );
}

static char bitlib_BL_Receive_doc[] = "BL_Receive(D,R,N,T) -> OK\n\n\
Receives up to N reply characters from device D (handle) returning them\n\
via string R subject to timeout T (in seconds). Returns OK true when\n\
successful, false otherwise. Replies are sent by the device in response\n\
to commands previously sent using BL_Send. Use BL_Count(D) to find out\n\
how many reply characters can be received without blocking.";
static PyObject * bitlib_BL_Receive ( PyObject * self, PyObject * args ) {
    char* array; int size, timeout;
	if (!PyArg_ParseTuple(args, "sii:BL_Receive", &array, &size, &timeout)) return NULL;
	if ( BL_Receive(array,size,timeout) ) Py_RETURN_TRUE; else Py_RETURN_FALSE;
}

static char bitlib_BL_Rate_doc[] = "BL_Rate(R) -> A\n\n\
Request a sample rate R (in Hz) and return duration A that will actually\n\
be used. They are usually the same but may differ if the available buffer\n\
(BL_Size) is insufficient for the capture duration (BL_Time).\n\
If R = 0 (or omitted) the prevailing sample rate is returned without change.";
static PyObject * bitlib_BL_Rate ( PyObject * self, PyObject * args ) {
	double rate = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|d:BL_Rate", &rate) ) return NULL;
	return PyFloat_FromDouble( BL_Rate(rate) );
}

static char bitlib_BL_Select_doc[] = "BL_Select(T,R) -> A\n\n\
Request the selection of a device, channel, range or source (R) where\n\
T is (0=>device,1=>channel,2=>source). If T is omitted the device is\n\
selected. Returns the selection (A) which is the same as R if successful.\n\
If R = -1 or omitted the current selection is returned.";
static PyObject * bitlib_BL_Select ( PyObject * self, PyObject * args ) {
	int T = BL_SELECT_DEVICE, R = BL_ASK;
	if ( !PyArg_ParseTuple(args, "|ii:BL_Select", &T, &R) ) return NULL;
	return PyInt_FromLong( BL_Select(T,R) );
}

static char bitlib_BL_Send_doc[] = "BL_Send(S,L)\n\n\
Send the command string S to the selected device on layer L (0=scope,\n\
1=>generator). This function can be used with BL_Receive to send and\n\
receive command strings to a device effectively bypassing the library.";
static PyObject * bitlib_BL_Send ( PyObject * self, PyObject * args ) {
	char* array; int layer = BL_ZERO;
	if (!PyArg_ParseTuple(args, "s|i:BL_Send", &array, &layer)) return NULL;
	BL_Send(array,layer);
	Py_RETURN_TRUE;
}

static char bitlib_BL_Index_doc[] = "BL_Index(R) -> A\n\n\
Request the capture address R and return the address actually used A\n\
which may be different if the request is unavailable or invalid. If\n\
R is omitted the address is (re)set to zero.";
static PyObject * bitlib_BL_Index ( PyObject * self, PyObject * args ) {
	int address = BL_ZERO;
	if ( !PyArg_ParseTuple(args, "|i:BL_Index", &address) ) return NULL;
	if ( BL_Index( address ) ) Py_RETURN_TRUE; else Py_RETURN_FALSE;
}

static char bitlib_BL_Delay_doc[] = "BL_Delay(S) -> OK\n\n\
Assigned S (seconds) as the post-triger delay. If S is 0 or omitted, disables delay.";
static PyObject * bitlib_BL_Delay ( PyObject * self, PyObject * args ) {
    double delay = BL_ZERO;
	if ( !PyArg_ParseTuple(args, "|d:BL_Delay", &delay) ) return NULL;
	return PyFloat_FromDouble( BL_Delay(delay) );
}

static char bitlib_BL_Offset_doc[] = "BL_Offset(R) -> A\n\n\
Request offset R and return the offset that is actually assigned to\n\
to the selected device, channel and source (BL_Select). If a value\n\
beyond the available offset range of the device is specified the\n\
closest available offset for that channel is used.";
static PyObject * bitlib_BL_Offset ( PyObject * self, PyObject * args ) {
	double value;
	if ( !PyArg_ParseTuple(args, "d:BL_Offset", &value) ) return NULL;
	return PyFloat_FromDouble( BL_Offset(value) );
}

static char bitlib_BL_Trigger_doc[] = "BL_Trigger(L,E) -> OK\n\n\
Assign L (volts) as the trigger level on edge E (0=>rise, 1=>fall).";
static PyObject * bitlib_BL_Trigger ( PyObject * self, PyObject * args ) {
	int edge = BL_TRIG_RISE; double level = BL_ZERO;
	if ( !PyArg_ParseTuple(args, "|di:BL_Trigger", &level, &edge) ) return NULL;
	if ( BL_Trigger(level,edge) ) Py_RETURN_TRUE; else Py_RETURN_FALSE;
}

static char bitlib_BL_Trace_doc[] = "BL_Trace(T,A) -> OK\nBL_Trace(T) -> OK\nBL_Trace() -> OK\n\n\
Commence capture subject to timeout T (seconds) and block until\n\
the trace completes unless A is true in which case return now\n\
and capture asynchronously. In the latter use BL_State()\n\
to determine the state of capture. Returns OK true if the trace\n\
commenced successfully, false otherwise. If T is zero or omitted,\n\
perform a forced trigger trace immediately. If T is negative, do\n\
the trace with infinite timeout but do it execute aysnchronously.";
static PyObject * bitlib_BL_Trace ( PyObject * self, PyObject * args ) {
	double timeout = BL_TRACE_FORCED; bool async = BL_SYNCHRONOUS;
	if ( !PyArg_ParseTuple(args, "|db:BL_Trace", &timeout, &async) ) return NULL;
	if ( BL_Trace(timeout,async) ) Py_RETURN_TRUE; else Py_RETURN_FALSE;
}

static char bitlib_BL_Version_doc[] = "BL_Version(T) -> V\n\n\
BL_Version(0) returns the version of the selected device.\n\
BL_Version(1) returns the version of library.\n\
BL_Version(2) returns the version of python binding.";
static PyObject * bitlib_BL_Version ( PyObject * self, PyObject * args ) {
	int selector = BL_VERSION_DEVICE; char * version = BL_PYTHON_VERSION;
	if (!PyArg_ParseTuple(args, "|i:BL_Version", &selector)) return NULL;
	if ( selector < BL_VERSION_BINDING ) version = BL_Version(selector);
	return PyString_FromFormat( version );
}

static PyMethodDef bitlib_methods[] = { /* method definition table */
	{"BL_Acquire",bitlib_BL_Acquire, METH_VARARGS, bitlib_BL_Acquire_doc},
	{"BL_Close",bitlib_BL_Close, METH_VARARGS, bitlib_BL_Close_doc},
	{"BL_Count",bitlib_BL_Count, METH_VARARGS, bitlib_BL_Count_doc},
	{"BL_Coupling",bitlib_BL_Coupling, METH_VARARGS, bitlib_BL_Coupling_doc},
	{"BL_Delay",bitlib_BL_Delay, METH_VARARGS, bitlib_BL_Delay_doc},
	{"BL_Enable",bitlib_BL_Enable, METH_VARARGS, bitlib_BL_Enable_doc},
	{"BL_Halt",bitlib_BL_Halt, METH_VARARGS, bitlib_BL_Halt_doc},
	{"BL_ID",bitlib_BL_ID, METH_VARARGS, bitlib_BL_ID_doc},
	{"BL_Index",bitlib_BL_Index, METH_VARARGS, bitlib_BL_Index_doc},
	{"BL_Initialize",bitlib_BL_Initialize, METH_VARARGS, bitlib_BL_Initialize_doc},
	{"BL_Intro",bitlib_BL_Intro, METH_VARARGS, bitlib_BL_Intro_doc},
	{"BL_Log",bitlib_BL_Log, METH_VARARGS, bitlib_BL_Log_doc},
	{"BL_Mode",bitlib_BL_Mode, METH_VARARGS, bitlib_BL_Mode_doc},
	{"BL_Name",bitlib_BL_Name, METH_VARARGS, bitlib_BL_Name_doc},
	{"BL_Offset",bitlib_BL_Offset, METH_VARARGS, bitlib_BL_Offset_doc},
	{"BL_Open",bitlib_BL_Open, METH_VARARGS, bitlib_BL_Open_doc},
	{"BL_Range",bitlib_BL_Range, METH_VARARGS, bitlib_BL_Range_doc},
	{"BL_Rate",bitlib_BL_Rate, METH_VARARGS, bitlib_BL_Rate_doc},
	{"BL_Receive",bitlib_BL_Receive, METH_VARARGS, bitlib_BL_Receive_doc},
	{"BL_Select",bitlib_BL_Select, METH_VARARGS, bitlib_BL_Select_doc},
	{"BL_Send",bitlib_BL_Send, METH_VARARGS, bitlib_BL_Send_doc},
	{"BL_Size",bitlib_BL_Size, METH_VARARGS, bitlib_BL_Size_doc},
	{"BL_State",bitlib_BL_State, METH_VARARGS, bitlib_BL_State_doc},
	{"BL_Time",bitlib_BL_Time, METH_VARARGS, bitlib_BL_Time_doc},
	{"BL_Trace",bitlib_BL_Trace, METH_VARARGS, bitlib_BL_Trace_doc},
	{"BL_Trigger",bitlib_BL_Trigger, METH_VARARGS, bitlib_BL_Trigger_doc},
	{"BL_Version",bitlib_BL_Version, METH_VARARGS, bitlib_BL_Version_doc},
	{NULL, NULL}
};

PyMODINIT_FUNC initbitlib ( void ) { /* initialise module */
	PyObject * module; int i, n;
	struct { char * N; int V; } T[] = {
		{"BL_ASK", BL_ASK},
		{"BL_ASYNCHRONOUS", BL_ASYNCHRONOUS},
		{"BL_COUNT_ANALOG", BL_COUNT_ANALOG},
		{"BL_COUNT_DEVICE", BL_COUNT_DEVICE},
		{"BL_COUNT_LOGIC", BL_COUNT_LOGIC},
		{"BL_COUNT_RANGE", BL_COUNT_RANGE},
		{"BL_MAX_RATE", BL_MAX_RATE},
		{"BL_MAX_SIZE", BL_MAX_SIZE},
		{"BL_MAX_TIME", BL_MAX_TIME},
		{"BL_MODE_FAST", BL_MODE_FAST},
		{"BL_MODE_DUAL", BL_MODE_DUAL},
		{"BL_MODE_LOGIC", BL_MODE_LOGIC},
		{"BL_MODE_MIXED", BL_MODE_MIXED},
		{"BL_MODE_STREAM", BL_MODE_STREAM},
		{"BL_SELECT_CHANNEL", BL_SELECT_CHANNEL},
		{"BL_SELECT_DEVICE", BL_SELECT_DEVICE},
		{"BL_SELECT_SOURCE", BL_SELECT_SOURCE},
		{"BL_SOURCE_ALT", BL_SOURCE_ALT},
		{"BL_SOURCE_BNC", BL_SOURCE_BNC},
		{"BL_SOURCE_GND", BL_SOURCE_GND},
		{"BL_SOURCE_POD", BL_SOURCE_POD},
		{"BL_SOURCE_X10", BL_SOURCE_X10},
		{"BL_SOURCE_X20", BL_SOURCE_X20},
		{"BL_SOURCE_X50", BL_SOURCE_X50},
		{"BL_COUPLING_DC", BL_COUPLING_DC},
		{"BL_COUPLING_AC", BL_COUPLING_AC},
		{"BL_COUPLING_RF", BL_COUPLING_RF},
		{"BL_STATE_ACTIVE", BL_STATE_ACTIVE},
		{"BL_STATE_DONE", BL_STATE_DONE},
		{"BL_STATE_ERROR", BL_STATE_ERROR},
		{"BL_STATE_IDLE", BL_STATE_IDLE},
		{"BL_SYNCHRONOUS", BL_SYNCHRONOUS},
		{"BL_TRACE_FORCED", BL_TRACE_FORCED},
		{"BL_TRACE_FOREVER", BL_TRACE_FOREVER},
		{"BL_TRIG_FALL", BL_TRIG_FALL},
		{"BL_TRIG_HIGH", BL_TRIG_HIGH},
		{"BL_TRIG_LOW", BL_TRIG_LOW},
		{"BL_TRIG_NONE", BL_TRIG_NONE},
		{"BL_TRIG_RISE", BL_TRIG_RISE},
		{"BL_VERSION_BINDING", BL_VERSION_BINDING},
		{"BL_VERSION_DEVICE", BL_VERSION_DEVICE},
		{"BL_VERSION_LIBRARY", BL_VERSION_LIBRARY},
		{"BL_ZERO", BL_ZERO}
	};
	module = Py_InitModule3("bitlib", bitlib_methods, bitlib_doc);
	n = sizeof(T) / sizeof(T[0]);
	for ( i = 0; i < n; i++ )
		PyModule_AddIntConstant(module,T[i].N, T[i].V);
}
