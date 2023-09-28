from NodoI import NodoI
import logging
import sys, traceback, Ice

if "--debug" in sys.argv:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


id = int(sys.argv[1])
logging.debug("id es: {}".format(id))

n = 3
status = 0
ic = None
try:
    ic = Ice.initialize()

    adapter = ic.createObjectAdapterWithEndpoints("NodoAdapter", "default -p 1000{}".format(id))
    object = NodoI(id)
    adapter.add(object, ic.stringToIdentity("Nodo_{}".format(id)))
    adapter.activate()

    object.daemon = True
    object.start()
    ic.waitForShutdown()

except:
    traceback.logging.debug_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.logging.debug_exc()
        status = 1

sys.exit(status)