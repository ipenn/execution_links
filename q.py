import quickfix
import sys

if len(sys.argv) < 2: 
	print "error"
fileName = sys.argv[1]

class MyApplication(_object):
        def onCreate(self, sessionID): return
        def onLogon(self, sessionID): return
        def onLogout(self, sessionID): return
        def toAdmin(self, message, sessionID): return
        def toApp(self, message, sessionID): return
        def fromAdmin(self, message, sessionID): return
        def fromApp(self, message, sessionID): return

try:
        settings = quickfix.SessionSettings(fileName)
        application = quickfix.MyApplication()
        storeFactory = quickfix.FileStoreFactory(settings)
        logFactory = quickfix.FileLogFactory(settings)
        acceptor = quickfix.SocketAcceptor(application, storeFactory, settings, logFactory)
        acceptor.start()
        # while condition == true: do something
        acceptor.stop()
except quickfix.ConfigError, e:
        print e