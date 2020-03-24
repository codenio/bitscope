/* report.c -- BitLib 2.0 Capture Device Report Generator (ANSI C)
 * See User Programming Manual for information about these calls.*/

#include <stdio.h>
#include <limits.h>
#include <bitlib.h> /* required */

#define MY_DEVICES 1 /* change this if you have more than one */
#define MY_PROBE_FILE "" /* default probe file if unspecified */

const char * MODES[] = {"FAST","DUAL","MIXED","LOGIC","STREAM"};
const char * SOURCES[] = {"POD","BNC","X10","X20","X50","ALT","GND"}; 

int main(int argc, char *argv[]) {
	int N;
   /* 
    * Open the first device found (only)
    */
    printf("\nStarting: Attempting to open %d device%s...",MY_DEVICES,MY_DEVICES!=1?"s":"");
	if ( (N = BL_Open(MY_PROBE_FILE,MY_DEVICES)) ) {
		int i;
	   /*
	    * Open succeeded, report library version and for each device...
	    */
		printf("\n Library: %s (report.c)\n",BL_Version(BL_VERSION_LIBRARY));
		printf("  Opened: %d Device%s\n",N,N!=1?"s":"");
		for ( i = 0; i < N; i++ ) {
			int j;
		   /*
		    * Select the device (all following functions talk to this device).
		    */
			BL_Select(BL_SELECT_DEVICE,i);
		   /*
		    * Report the device, link and available channels.
		    */
			printf("\nBitScope: %s (%s)\n",BL_ID(),BL_Version(BL_VERSION_DEVICE));
			{ char name[100]; printf("    Link: %s\n",BL_Name(name)); }
			printf("Channels: %d (%d analog + %d logic)\n",
				   BL_Count(BL_COUNT_ANALOG)+BL_Count(BL_COUNT_LOGIC),
				   BL_Count(BL_COUNT_ANALOG),BL_Count(BL_COUNT_LOGIC));
		   /*
		    * Determine which modes the device supports.
		    */
			printf("   Modes:");
			for ( j = BL_MODE_FAST; j <= BL_MODE_STREAM; j++ )
				if ( BL_Mode(j) == j ) printf(" %s",MODES[j]);
		   /*
		    * Report canonic capture specification in LOGIC (if supported) or FAST mode (otherwise).
		    */
			if ( BL_Mode(BL_MODE_LOGIC) == BL_MODE_LOGIC || BL_Mode(BL_MODE_FAST) == BL_MODE_FAST ) 
				printf("\n Capture: %d @ %.0fHz = %fs (%s)\n",BL_Size(BL_ASK),
					   BL_Rate(BL_ASK), BL_Time(BL_ASK),MODES[BL_Mode(BL_ASK)]);
		   /*
		    * Report the maximum offset range (if the device supports offsets).
		    */
			BL_Range(BL_Count(BL_COUNT_RANGE)); /* highest range */
			if ( BL_Offset(INT_MIN) != BL_Offset(INT_MAX) ) /* supports offsets */
				printf("  Offset: %+.4gV to %+.4gV\n",BL_Offset(INT_MAX), BL_Offset(INT_MIN));
		   /*
			* Report the sources provided by the device and their respective ranges.
			*/
			for ( j = BL_SOURCE_POD; j <= BL_SOURCE_GND; j++ ) {
				int k, n = BL_Count(BL_COUNT_RANGE);
				if ( j == BL_Select(BL_SELECT_SOURCE,j) ) {
					printf("     %s:",SOURCES[j]);
					for ( k = n-1; k >= 0; k-- )
						printf(" %5.2fV",BL_Range(k));
					printf("\n");
				}
			}
		}
	}
	printf("\n");
	BL_Close();
	return 0;
}
