import pyclamd

daemon = pyclamd.PyClamd(verbose = True)

print daemon.getVersion()
print daemon.getStatus()

