;========================================================================
; Program: 8051 MCU - Seven Segment Display Multiplex
; 
; Created     : Mar 12 2024
; Author      : Diego Souza (original example by from Prof. Vooi Yap)
; Processor   : AT89S52 (With 11.0592MHz EXTERNAL Crystal)
; Compiler    : M-IDE Studio for MCS-51
; Simulator   : SimulIDE 1.1.0 SR0
;
; Description: This program multiplexes a 00 to 99 counter
; on two 7-segment displays with an specific
; time interval. Note: a logic 0 lights a display segment.
;========================================================================
;========================================================================
; INSTRUCTIONS USED (https://www.win.tue.nl/~aeb/comp/8051/set8051.html)
; EQU (equate): This is used to define a constant without 
; occupying a memory location.
; MOVC: Move Code Byte to Accumulator. MOVC moves a byte from Code Memory 
; into the Accumulator. The Code Memory address from which the byte will 
; be moved is calculated by summing the value of the Accumulator 
; with either DPTR or the Program Counter (PC)
; SJMP: Short Jump - SJMP jumps unconditionally to the address specified
; must be within -128 or +127 bytes of the instruction that follows.
; ACALL: Absolute Call Within 2K Block - unconditionally calls a 
; subroutine at the indicated code address
; CLR: Clear Register
; SETB: Set Bit
; CJNE: Compare and Jump If Not Equal
; DJNZ: Decrement and Jump if Not Zero
;========================================================================
;========================================================================
; RESET VECTOR
;========================================================================
	ORG	000H          ; Reset vector address

;========================================================================
; DEFINITIONS
;========================================================================
EN_DP1	EQU	P2.6	      ; Enable pin - Display 1
EN_DP2	EQU	P2.5	      ; Enable pin - Display 2

;========================================================================
; VARIABLES
;========================================================================
	MOV	DPTR,#LUT     ; DPTR points to the start of the lookup table
	MOV	R0,#00H       ; Init the tens
	MOV	R1,#00H       ; Init the ones
	MOV	R3,#00H       ; Init our time reference

;========================================================================
; CODE SEGMENT
;========================================================================

; Main function	
MAIN:

BACK:
	; Show digit on display 1
	CLR	EN_DP1        ; Enable display 1
	SETB	EN_DP2        ; Disable display 2

	MOV 	A,R0          ; Digit to show on display 1
	ACALL 	DISPLAY       ; Show the digit

	MOV 	R7,#5         ; 5 ms interval
	ACALL 	DELAY         ; Call the delay subroutine

	; Show digit on display 2
	SETB 	EN_DP1        ; Disable display 1
	CLR 	EN_DP2        ; Enable display 2

	MOV 	A,R1          ; Digit to show on display 2
	ACALL 	DISPLAY       ; Show the digit

	MOV 	R7,#5         ; 5 ms interval
	ACALL 	DELAY         ; Call the delay subroutine
	
	; Time reference
	INC 	R3            ; Increment R3 (our time reference)
	CJNE 	R3,#100, BACK ; If R3 is not equal to 50 (100 x 2 x 5 ms = 1s), jump to back
	MOV 	R3,#0         ; If R3 is equal to 50, reset our time reference
 	
 	; Ones
 	INC 	R1            ; and increment R1 (ones)
 	CJNE 	R1,#10, BACK  ; If R1 (ones) is not equal to 10, jump to back
	MOV 	R1,#0         ; If R1 (ones) is equal to 10, zero the ones
	
	; Tens
	INC 	R0            ; and increment R0 (tens)
	CJNE 	R0,#10, BACK  ; If R0 (tens) is not equal to 10, jump to back
	MOV 	R0,#0         ; If R0 (tens) is equal to 10, zero the tens

	SJMP 	MAIN          ; Jump back to the start 

;========================================================================
; DISPLAY:  Subroutine to Display Decimal Numbers ( 0 to 9)
; Data Index is defined in A (Accumulator)
; Data Pattern Bytes are stored in  Program Memory as DB  
; Data Pointer Directive used to Access Addresses
;========================================================================
; Display function
DISPLAY: 
	MOVC	A,@A+DPTR     ; Gets digit drive pattern for the current value from LUT
 	MOV	P0,A          ; Puts corresponding digit drive pattern into P1
	RET                   ; Return from subroutine

; Delay function
DELAY:  
	MOV	R2,#230       ; 2 cycles
LOOP: 
	NOP                   ; 1 cycles
	NOP                   ; 1 cycles
	DJNZ	R2, LOOP      ; 2 cycles consume 230x4 + 2 instr cycles = 922 cycles
	DJNZ	R7, DELAY     ; 922 cycles (which is equal to 1 ms) * number of counts in R7  
	RET                   ; Return from subroutine

;========================================================================
; Data Patterns Stored here (Common Anode 7 Segment Display)
;========================================================================
	ORG	0200h
LUT:	
	DB	0C0h, 0F9h, 0A4h, 0B0h, 099h, 092h, 082h, 0F8h, 080h, 090h, 0
;========================================================================

	END                   ; End of Program
;========================================================================
; ----------------------END of the Assembly Program----------------------
;========================================================================