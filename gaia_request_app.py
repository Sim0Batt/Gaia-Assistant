from gaia import Gaia as g
import sys


gaia_ref = g()

if len(sys.argv) != 2:
    print("errore: nessuna variable letta")
    sys.exit(1)

request = sys.argv[1]

gaia_ref.get_response(str(request))

