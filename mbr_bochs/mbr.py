"""
A sample loader script for loading MBR and symbols (from map files)
After the loading process one can easily debug the MBR with IDA Bochs plugin
(c) Hex-Rays
"""
import sys
import os
import re

# --------------------------------------------------------------------------
# Some constants
SECTOR_SIZE = 512
BOOT_START  = 0x7C00
BOOT_SIZE   = 0x7C00 + SECTOR_SIZE * 2
BOOT_END    = BOOT_START + BOOT_SIZE
SECTOR2     = BOOT_START + SECTOR_SIZE
MBRNAME    = "mbr"
IMGNAME     = "c.img"

# --------------------------------------------------------------------------
def ParseMap(map_file):
    """
    Opens and parses a map file
    Returns a list of tuples (addr, addr_name) or an empty list on failure
    """
    ret = []
    f = open(map_file)
    if not f:
        return ret
    # look for the beginning of symbols
    for line in f:
        if line.startswith("Real"):
            break
    else:
        return ret
    # Prepare RE for the line of the following form:
    # 7C1F              7C1F  io_error
    r = re.compile('\s*(\w+)\s*(\w+)\s*(\w*)')

    for line in f:
        m = r.match(line.strip())
        if not m:
            continue
        ret.append((int(m.group(2), 16), m.group(3)))
    return ret

# --------------------------------------------------------------------------
def UpdateImage(imgfile, mbrfile):
  """
  Write the MBR code into the disk image
  """
  
  # open image file
  f = open(imgfile, "r+b")
  if not f:
    print "Could not open image file!"
    return False
  # open MBR file
  f2 = open(mbrfile, "rb")
  if not f2:
    print "Could not open mbr file!"
    return False

  # read whole MBR file
  mbr = f2.read()
  f2.close()

  # update image file
  f.write(mbr)
  f.close()

  return True
    
# --------------------------------------------------------------------------
def MbrLoader():
    """ 
    This small routine loads the MBR into IDA
    It acts as a custom file loader (written with a script)
    """
    import idaapi;
    import idc;

    global SECTOR_SIZE, BOOT_START, BOOT_SIZE, BOOT_END, SECTOR2, MBRNAME

    # wait till end of analysis
    idc.Wait()

    # adjust segment
    idc.SetSegBounds(BOOT_START, BOOT_START, BOOT_START + BOOT_SIZE, idaapi.SEGMOD_KEEP)

    # load the rest of the MBR
    idc.loadfile(MBRNAME, SECTOR_SIZE, SECTOR2, SECTOR_SIZE)

    # Make code
    idc.AnalyzeArea(BOOT_START, BOOT_END)

# --------------------------------------------------------------------------
def ApplySymbols():
    """
    This function tries to apply the symbol names in the database
    If it succeeds it prints how many symbol names were applied
    """
    global MBRNAME
    map_file = MBRNAME + ".map"
    if not os.path.exists(map_file):
        return
    syms = ParseMap(map_file)
    if not len(syms): 
        return

    for sym in syms:
        MakeNameEx(sym[0], sym[1], SN_CHECK|SN_NOWARN)
    
    print "Applied %d symbol(s)" % len(syms)

# --------------------------------------------------------------------------
def UserInit():
    """
    Use this function to do additional tasks after the loading process
    In this case, we will add a breakpoint after the complete MBR is loaded
    """
    idc.AddBpt(idc.LocByName("MBR_LOADED"))

# --------------------------------------------------------------------------
# Main

# Executed from command line?
if len(sys.argv) > 1:
    if UpdateImage(IMGNAME, MBRNAME):
        print "Updated image file successfully!"
        sys.exit(0)
    else:
        print "Failed to update image file!"
        sys.exit(1)
# Executed from IDA?
else:
    MbrLoader()
    ApplySymbols()
    UserInit()

    # Exit IDA
    idc.Exit(0)
