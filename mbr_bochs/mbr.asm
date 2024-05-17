;--------------------------------------------------------------------------
; MBR sample #1
;
; (c) Hex-Rays.com
;--------------------------------------------------------------------------

%define CRT_VIDEO_MODE3_ROWS    25
%define CRT_VIDEO_MODE3_COLS    80

%define BOOT_START              0x7C00
%define SECTOR_SIZE             512
%define BOOT_SECTOR_SIZE        SECTOR_SIZE * 2
%define BOOT_STACK_SIZE         512 
%define BOOT_SP                 (BOOT_START + BOOT_SECTOR_SIZE + BOOT_STACK_SIZE - 2)

[bits 16]
[org BOOT_START]

; generate a map file
[map symbols mbr.map]

begin:
   ; setup all segments
   xor ax, ax
   mov ds, ax
   mov es, ax
   mov ss, ax
   mov sp, BOOT_SP

   ; let's load the rest of the mbr
   call load_code
MBR_LOADED:
   ; clear bios boot text
   call clear_screen

   ; show loading message
   mov bl, 0x5

 .for_next:
   push bx
   mov si, data.msg_welcome
   call write_str 
   pop bx
   inc bx
   cmp bl, 0xf
   jl short .for_next

   ; run code from 2nd sector
   call welcome2

   jmp  $

;--------------------------------------------------------------------------
; displays an error message and halts
;--------------------------------------------------------------------------
io_error:
   mov si, data.msg_ioerror
   mov bl, 4
   call write_str
   jmp $

;--------------------------------------------------------------------------
; loads bootsector remaining code into the 0x7C00+0x200 and on address
;--------------------------------------------------------------------------
load_code:
   mov ah, 0x02
   mov al, 1 ; number of sectors
   mov cx, 0x0002 ; 2nd sector
   mov dx, 0x0080
   mov bx, BOOT_START + SECTOR_SIZE
   int 0x13
   jnc .ret
   call io_error
  .ret:
   ret

;--------------------------------------------------------------------------
; clears the screen by switching to mode 3
; ->it also reset the writing cursor position
;--------------------------------------------------------------------------
clear_screen:
  mov ax, 0x0003
  int 0x10
  mov word [crt_data.line_col], 0
  ret

;--------------------------------------------------------------------------
; writes a line to the screen
; directly to the video segment
; bl = color
; ds:si = string
;--------------------------------------------------------------------------
write_str:
 .next:
  mov dl, byte [crt_data.line_col]
  cmp dl, CRT_VIDEO_MODE3_COLS
  jl  .check_row
  call .next_row
 .check_row:
  mov dh, byte [crt_data.line_row]
  cmp dh, CRT_VIDEO_MODE3_ROWS
  jl  .check_char
  call .start_over
 .check_char:
  lodsb
  test al, al
  jz .done
  cmp al, 0xd
  jnz .print_char
  call .next_row
  jmp short .next
 .print_char:
  mov bh, 0
  mov ah, 2
  int 0x10
  mov ah, 9
  mov cx, 1
  int 0x10
  inc byte [crt_data.line_col]
  jmp short .next
 .start_over:
  mov word [crt_data.line_col], 0
  xor dx, dx
  ret
 .next_row:
  mov dl, 0
  mov byte [crt_data.line_col], dl
  inc byte [crt_data.line_row]
  inc dh
 .done:
  ret
crt_data:
  .line_col db 0
  .line_row db 0

;--------------------------------------------------------------------------
data:
  .msg_ioerror  db "Could not read sectors! Halted!",0
  .msg_welcome  db 'This is our boot sector', 0xd, 0
;--------------------------------------------------------------------------
 times 512-2-($-$$) db 0  ; fill sector w/ 0's
 db 0x55          ; req'd by some BIOSes
 db 0xAA
;--------------------------------------------------------------------------

;--------------------------------------------------------------------------
; MBR / 2nd sector
;--------------------------------------------------------------------------
sector2:

;--------------------------------------------------------------------------
; displays a message
;--------------------------------------------------------------------------
welcome2:
  mov si, data2.msg_welcome
  mov  bl, 0xE
  call write_str

  ret

data2:
.msg_welcome db "Welcome from 2nd sector code!", 0xd, 0

times 512-($-sector2) db 0  ; fill sector w/ 0's
