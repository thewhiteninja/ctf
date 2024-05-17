from winappdbg import Debug, EventHandler
import sys

def change_key( event ):
    process = event.get_process()
    thread  = event.get_thread()
    registers  = thread.get_context()
    keyAddr   = registers['Eax']
    process.write(keyAddr, chr(current_key))      
       
def read_genkey( event ):
    global current_key
    process = event.get_process()
    thread  = event.get_thread()
    registers  = thread.get_context()
    keyAddr   = registers['Eax']
    value = process.read( keyAddr, 80 )
    print "%s : %s"%(hex(current_key), value.encode("hex"))
    current_key += 1
    sys.stdout.flush()
    process.kill()

class MyEventHandler( EventHandler ):
    def create_process( self, event ):
        pid = event.get_pid()
        event.debug.break_at( pid, 0x0040284E, change_key )
        event.debug.break_at( pid, 0x00403593, read_genkey )

debug = Debug( MyEventHandler(), bKillOnExit = True)
current_key = 0x00
while current_key < 0x100:
    try:
        debug.execv( ["cryptochief.exe"] )
        debug.loop()
    except:
        pass


