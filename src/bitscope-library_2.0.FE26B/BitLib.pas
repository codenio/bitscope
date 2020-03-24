unit BitLib; { BitScope Library Version 2.0 (FE26B) }

interface

const

  BL_MAX_RATE = 0;
  BL_MAX_TIME = 0;
  BL_MAX_SIZE = 0;
  BL_TRACE_FORCED = 0;
  BL_TRACE_FOREVER = -1;
  BL_ZERO = 0;
  BL_ASK = -1;
  
  BL_COUNT_DEVICE = 0;
  BL_COUNT_ANALOG = 1;
  BL_COUNT_LOGIC = 2;
  BL_COUNT_RANGE = 3;

  BL_SELECT_DEVICE = 0;
  BL_SELECT_CHANNEL = 1;
  BL_SELECT_SOURCE = 2;

  BL_STATE_IDLE = 0;
  BL_STATE_ACTIVE = 1;
  BL_STATE_DONE = 2;
  BL_STATE_ERROR = 3;
  
  BL_SOURCE_POD = 0;
  BL_SOURCE_BNC = 1;
  BL_SOURCE_X10 = 2;
  BL_SOURCE_X20 = 3;
  BL_SOURCE_X50 = 4;
  BL_SOURCE_ALT = 5;
  BL_SOURCE_GND = 6;

  BL_COUPLING_DC = 0;
  BL_COUPLING_AC = 1;
  BL_COUPLING_RF = 2;

  BL_MODE_FAST = 0;
  BL_MODE_DUAL = 1;
  BL_MODE_MIXED = 2;
  BL_MODE_LOGIC = 3;
  BL_MODE_STREAM = 4;
  
  BL_TRIG_RISE = 0;
  BL_TRIG_FALL = 1;
  BL_TRIG_HIGH = 2;
  BL_TRIG_LOW = 3;
  BL_TRIG_NONE = 4;
  
  BL_VERSION_DEVICE = 0;
  BL_VERSION_LIBRARY = 1;
  BL_VERSION_BINDING = 2;
  BL_VERSION_PLATFORM = 3;
  BL_VERSION_FRAMEWORK = 4;
  BL_VERSION_NETWORK = 5;

  BL_SYNCHRONOUS = 0;
  BL_ASYNCHRONOUS = 1;
        
{$ifdef MSWINDOWS}
  {$ifdef StdCall}
  function BL_Acquire(ASize : Integer; AData : PDouble) : Integer; stdcall; external 'BitLib.dll';
  procedure BL_Close; stdcall; external 'BitLib.dll';
  function BL_Count(AType : Integer = BL_ASK) : Integer; stdcall; external 'BitLib.dll';
  function BL_Coupling(ACoupling : Integer = BL_ASK) : Integer; stdcall; external 'BitLib.dll';
  function BL_Delay(ADelayTime : Double) : Double; stdcall; external 'BitLib.dll';
  function BL_Enable( AEnable : Boolean) : Boolean; stdcall; external 'BitLib.dll';
  function BL_Error : Integer; stdcall; external 'BitLib.dll';
  function BL_Halt : Boolean; stdcall; external 'BitLib.dll';
  function BL_ID : PAnsiChar; stdcall; external 'BitLib.dll';
  function BL_Index(AAddr : Integer) : Boolean; stdcall; external 'BitLib.dll';
  procedure BL_Initialize; stdcall; external 'BitLib.dll';
  function BL_Intro(APreTrigger : Double) : Double; stdcall; external 'BitLib.dll';
  function BL_Log : PAnsiChar; stdcall; external 'BitLib.dll';
  function BL_Mode(AMode : Integer) : Integer; stdcall; external 'BitLib.dll';
  function BL_Name(AStr : PAnsiChar) : PAnsiChar; stdcall; external 'BitLib.dll';
  function BL_Offset(AValue : Double) : Double; stdcall; external 'BitLib.dll';
  function BL_Open(AProbeStr : PAnsiChar; ACount : Integer = 1) : Integer; stdcall; external 'BitLib.dll';
  function BL_Range( AIndex : Integer ) : Double; stdcall; external 'BitLib.dll';
  function BL_Rate(ASampleRate : Double = BL_ASK) : Double; stdcall; external 'BitLib.dll';
  function BL_Receive(AStr : PAnsiChar; ASize : Integer; ATimeOut : Integer = 0) : Boolean; stdcall; external 'BitLib.dll';
  function BL_Select(AType : Integer; AIndex : Integer) : Integer; stdcall; external 'BitLib.dll';
  procedure BL_Send(AStr : PAnsiChar; ALayer : Integer = 0 ); stdcall; external 'BitLib.dll';
  function BL_Size(ASize : Integer = BL_ASK) : Integer; stdcall; external 'BitLib.dll';
  function BL_State : Integer; stdcall; external 'BitLib.dll';
  function BL_Time(ACaptureTime : Double = BL_ASK) : Double; stdcall; external 'BitLib.dll';
  function BL_Trace(ATimeOut : Double = BL_TRACE_FORCED; ASync : Boolean = False) : Boolean; stdcall; external 'BitLib.dll';
  function BL_Trigger(ALevel : Double; AEdge : Integer) : Boolean; stdcall;external 'BitLib.dll';
  function BL_Version(ATarget : Integer = BL_VERSION_DEVICE) : PAnsiChar; stdcall; external 'BitLib.dll';
  {$else}
  function BL_Acquire(ASize : Integer; AData : PDouble) : Integer; cdecl; external 'BitLib.dll';
  procedure BL_Close; cdecl; external 'BitLib.dll';
  function BL_Count(AType : Integer = BL_ASK) : Integer; cdecl; external 'BitLib.dll';
  function BL_Coupling(ACoupling : Integer = BL_ASK) : Integer; cdecl; external 'BitLib.dll';
  function BL_Delay(ADelayTime : Double) : Double; cdecl; external 'BitLib.dll';
  function BL_Enable( AEnable : Boolean) : Boolean; cdecl; external 'BitLib.dll';
  function BL_Error : Integer; cdecl; external 'BitLib.dll';
  function BL_Halt : Boolean; cdecl; external 'BitLib.dll';
  function BL_ID : PAnsiChar; cdecl; external 'BitLib.dll';
  function BL_Index(AAddr : Integer) : Boolean; cdecl; external 'BitLib.dll';
  procedure BL_Initialize; cdecl; external 'BitLib.dll';
  function BL_Intro(APreTrigger : Double) : Double; cdecl; external 'BitLib.dll';
  function BL_Log : PAnsiChar; cdecl; external 'BitLib.dll';
  function BL_Mode(AMode : Integer) : Integer; cdecl; external 'BitLib.dll';
  function BL_Name(AStr : PAnsiChar) : PAnsiChar; cdecl; external 'BitLib.dll';
  function BL_Offset(AValue : Double) : Double; cdecl; external 'BitLib.dll';
  function BL_Open(AProbeStr : PAnsiChar; ACount : Integer = 1) : Integer; cdecl; external 'BitLib.dll';
  function BL_Range( AIndex : Integer ) : Double; cdecl; external 'BitLib.dll';
  function BL_Rate(ASampleRate : Double = BL_ASK) : Double; cdecl; external 'BitLib.dll';
  function BL_Receive(AStr : PAnsiChar; ASize : Integer; ATimeOut : Integer = 0) : Boolean; cdecl; external 'BitLib.dll';
  function BL_Select(AType : Integer; AIndex : Integer) : Integer; cdecl; external 'BitLib.dll';
  procedure BL_Send(AStr : PAnsiChar; ALayer : Integer = 0 ); cdecl; external 'BitLib.dll';
  function BL_Size(ASize : Integer = BL_ASK) : Integer; cdecl; external 'BitLib.dll';
  function BL_State : Integer; cdecl; external 'BitLib.dll';
  function BL_Time(ACaptureTime : Double = BL_ASK) : Double; cdecl; external 'BitLib.dll';
  function BL_Trace(ATimeOut : Double = BL_TRACE_FORCED; ASync : Boolean = False) : Boolean; cdecl; external 'BitLib.dll';
  function BL_Trigger(ALevel : Double; AEdge : Integer) : Boolean; cdecl;external 'BitLib.dll';
  function BL_Version(ATarget : Integer = BL_VERSION_DEVICE) : PAnsiChar; cdecl; external 'BitLib.dll';  
  {$endif}
{$endif}
  
{$ifdef UNIX}
  function BL_Acquire(ASize : Integer; AData : PDouble) : Integer; cdecl; external 'libBitLib.so';
  procedure BL_Close; cdecl; external 'libBitLib.so';
  function BL_Count(AType : Integer = BL_ASK) : Integer; cdecl; external 'libBitLib.so';
  function BL_Coupling(ACoupling : Integer = BL_ASK) : Integer; cdecl; external 'libBitLib.so';
  function BL_Delay(ADelayTime : Double) : Double; cdecl; external 'libBitLib.so';
  function BL_Enable( AEnable : Boolean) : Boolean; cdecl; external 'libBitLib.so';
  function BL_Error : Integer; cdecl; external 'libBitLib.so';
  function BL_Halt : Boolean; cdecl; external 'libBitLib.so';
  function BL_ID : PAnsiChar; cdecl; external 'libBitLib.so';
  function BL_Index(AAddr : Integer) : Boolean; cdecl; external 'libBitLib.so';
  procedure BL_Initialize; cdecl; external 'libBitLib.so';
  function BL_Intro(APreTrigger : Double) : Double; cdecl; external 'libBitLib.so';
  function BL_Log : PAnsiChar; cdecl; external 'libBitLib.so';
  function BL_Mode(AMode : Integer) : Integer; cdecl; external 'libBitLib.so';
  function BL_Name(AStr : PAnsiChar) : PAnsiChar; cdecl; external 'libBitLib.so';
  function BL_Offset(AValue : Double) : Double; cdecl; external 'libBitLib.so';
  function BL_Open(AProbeStr : PAnsiChar; ACount : Integer = 1) : Integer; cdecl; external 'libBitLib.so';
  function BL_Range( AIndex : Integer ) : Double; cdecl; external 'libBitLib.so';
  function BL_Rate(ASampleRate : Double = BL_ASK) : Double; cdecl; external 'libBitLib.so';
  function BL_Receive(AStr : PAnsiChar; ASize : Integer; ATimeOut : Integer = 0) : Boolean; cdecl; external 'libBitLib.so';
  function BL_Select(AType : Integer; AIndex : Integer) : Integer; cdecl; external 'libBitLib.so';
  procedure BL_Send(AStr : PAnsiChar; ALayer : Integer = 0 ); cdecl; external 'libBitLib.so';
  function BL_Size(ASize : Integer = BL_ASK) : Integer; cdecl; external 'libBitLib.so';
  function BL_State : Integer; cdecl; external 'libBitLib.so';
  function BL_Time(ACaptureTime : Double = BL_ASK) : Double; cdecl; external 'libBitLib.so';
  function BL_Trace(ATimeOut : Double = BL_TRACE_FORCED; ASync : Boolean = False) : Boolean; cdecl; external 'libBitLib.so';
  function BL_Trigger(ALevel : Double; AEdge : Integer) : Boolean; cdecl; external 'libBitLib.so';
  function BL_Version(ATarget : Integer = BL_VERSION_DEVICE) : PAnsiChar; cdecl; external 'libBitLib.so';
{$endif}

implementation    

end.
