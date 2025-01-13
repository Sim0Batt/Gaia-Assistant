from gaia import Gaia as g
import sys

if len(sys.argv) != 2:
    print("errore: nessuna variable letta")
    sys.exit(1)

request = sys.argv[1]

g.GetResponse(str(request))

