import atexit
import logging as log

import receptor
log.basicConfig(level=log.DEBUG)

receptor.start()

@atexit.register
def exitHandler():
    receptor.stop()
