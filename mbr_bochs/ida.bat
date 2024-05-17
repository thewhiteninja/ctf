@echo off
  rem Debug MBR code with IDA/Bochs
  rem (c) Hex-Rays

  rem Assemble the MBR
  if exist mbr del mbr
  nasmw -f bin mbr.asm
  if not exist mbr goto end

  rem Update the image file
  python mbr.py update
  if not errorlevel 0 goto end

  rem Run IDA to load the file
  idaw -c -A -OIDAPython:mbr.py bochsrc

  rem database was not created
  if not exist bochsrc.idb goto end

  if exist mbr del mbr
  if exist mbr.map del mbr.map

  rem delete old database
  if exist mbr.idb del mbr.idb

  rem rename to mbr
  ren bochsrc.idb mbr.idb

  rem Start idag (without debugger)
  rem start idag mbr

  rem Start IDAG with debugger directly
  start idag -rbochs mbr

  echo Ready to debug with IDA Bochs
:end
