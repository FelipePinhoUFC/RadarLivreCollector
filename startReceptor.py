import atexit

import receptor

receptor.start()

@atexit.register
def exitHandler():
    receptor.stop()
