import socket
import os
import sys

class PyClamd:
    def __init__(self, ipc_socket_path = "/var/run/clamav/clamd.ctl", verbose = False):
        self.__buffer = 1024

        self.__verbose_mode = verbose
        self.__verbose_writer("Notice! Verbose has been enabled for PyClamd")
        self.__verbose_writer("Please use the setVerbose() function to turn it off if needed")

        self.__socket_client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.__verbose_writer("Created socket client")

        self.__ipc_socket_path = ipc_socket_path
        if not self.__does_file_exist(self.__ipc_socket_path): self.socketDoesNotExistException()
        
    def isVerbose(self):
        return self.__verbose_mode

    def setVerbose(self, verbose):
        self.__verbose_mode = verbose
        if verbose: self.__verbose_writer("PyClamd is now verbose")

    def getSocketBuffer(self):
        return self.__buffer

    def setSocketBuffer(self, bytes):
        self.__buffer = bytes    
        self.__verbose_writer("Set socket buffer to %d bytes in length" % bytes)

    def getUnixSocket(self):
        return self.__ipc_socket_path

    def setUnixSocket(self, socket_path):
        if not self.__does_file_exist(socket_path):
            raise SocketDoesNotExistException(socket_path)
        else:
            self.__ipc_socket_path = socket_path
            self.__verbose_writer("Socket has been set to %s" % socket_path)

    def __socketConnect(self):
        return self.__socket_client.connect(self.__ipc_socket_path)

    def __socketDisconnect(self):
        return self.__socket_client.close()

    def __socketSend(self, data):
        self.__socketConnect()
        self.__socket_client.send("n%s\n" % data)
        pending = self.__socket_client.recv(self.__buffer)
        self.__socketDisconnect()
        return pending

    def __does_file_exist(self, file_path):
        self.__verbose_writer("Checking to see if file '%s' exists" % file_path)
        return os.path.exists(file_path)

    def __verbose_writer(self, message):
        if self.__verbose_mode: sys.stdout.write("%s\n" % message)


    def ping(self):
        return self.__socketSend("PING")

    def getStatus(self):
        return self.__socketSend("STATUS")

    def getVersion(self):
        return self.__socketSend("VERSION")

    def reloadClamd(self):
        return self.__socketSend("RELOAD")

    def isFileVirus(self, file_path):
        if self.__does_file_exist(file_path):
            return "FOUND" in self.__socketSend("SCAN %s" % file_path)
        else: self.socketDoesNotExistException()
        
    def socketDoesNotExistException(self):
        raise Exception("UNIX Socket %s does not exist!" % self.__ipc_socket_path)
        
