program Report; { BitLib 2.0 Capture Device Report Generator (FPC)
See User Programming Manual for information about these calls.}

uses
  BitLib;

const
  MY_DEVICES = 1; { change this if you have more than one }
  MY_PROBE_FILE = ''; { default probe file if unspecified }

  MODES : array [BL_MODE_FAST..BL_MODE_STREAM] of string = ('FAST','DUAL','MIXED','LOGIC','STREAM');
  SOURCES : array [BL_SOURCE_POD..BL_SOURCE_GND] of string = ('POD','BNC','X10','X20','X50','ALT','GND');

var
  M, N, I, J, K : Integer;
  S : string;

begin
  WriteLn('Starting: Attempting to open ',MY_DEVICES,' device...');
  if BL_Open(MY_PROBE_FILE,MY_DEVICES) > 0 then begin
    {
      Open succeeded, report library version and for each device...
    }
    WriteLn(' Library: ',BL_Version(BL_VERSION_LIBRARY),' (report.pas)');
    N := BL_Count(BL_COUNT_DEVICE);
    WriteLn('  Opened: ',N,' Device');
    for I := 0 to N - 1 do begin
      {
        Select the device (all following functions talk to this device).
      }
      BL_Select(BL_SELECT_DEVICE,I);
      {
        Report the device, link and available channels.
      }
      WriteLn('BitScope: ',BL_ID(),' (',BL_Version(BL_VERSION_DEVICE),')');
      SetLength(S,100); WriteLn('    Link: ',BL_Name(PChar(S)));
      WriteLn('Channels: ',BL_Count(BL_COUNT_ANALOG)+BL_Count(BL_COUNT_LOGIC),
        ' (',BL_Count(BL_COUNT_ANALOG),' analog + ',BL_Count(BL_COUNT_LOGIC),' logic)');
      {
        Determine which modes the device supports.
      }
      Write('   Modes:');
      for J := BL_MODE_FAST to BL_MODE_STREAM do
        if BL_Mode(J) = J then Write(' ',MODES[J]);
      WriteLn;
      {
        Report canonic capture specification in LOGIC (if supported) or FAST mode (otherwise).
      }
      if (BL_Mode(BL_MODE_LOGIC) = BL_MODE_LOGIC) or (BL_Mode(BL_MODE_FAST) = BL_MODE_FAST ) then
        WriteLn(' Capture: ',BL_Size(BL_ASK),' @ ',BL_Rate(BL_ASK):5,'Hz = ',
          BL_Time(BL_ASK):5,'s (',MODES[BL_Mode(BL_ASK)],')');
      {
        Report the maximum offset range (if the device supports offsets).
      }
      BL_Range(BL_Count(BL_COUNT_RANGE)); { highest range }
      if BL_Offset(-MaxInt) <> BL_Offset(MaxInt) then { supports offsets }
        WriteLn('  Offset:',BL_Offset(MaxInt):5,'V to ',BL_Offset(-MaxInt):5,'V');
      {
        Report the sources provided by the device and their respective ranges.
      }
      for J := BL_SOURCE_POD to BL_SOURCE_GND do begin
        M := BL_Count(BL_COUNT_RANGE);
        if J = BL_Select(BL_SELECT_SOURCE,J) then begin
          Write('     ',SOURCES[J],':');
          for k := M-1 downto 0 do
            Write(BL_Range(K):5,'V');
          WriteLn
        end
      end
    end
  end;
  BL_Close();
end.
