"""  Print GPIO information on Raspberry Pi devices """

import sys
import pprint

try:
    # ignore this error as development happens primarily on non-RPi devices
    # pylint: disable=import-error
    from RPi import GPIO

except RuntimeError:
    print("Error importing RPi.GPIO. Elevated privileges may be required.")
    sys.exit(1)

# configure PrettyPrinter and print GPIO information
pprint.pp(GPIO.RPI_INFO, indent=2, width=80, compact=False, sort_dicts=True)
