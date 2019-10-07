import sys
import decimal

d = {
    "dict": dict(),
    "tuple": tuple(),
    "list": list(),
    "object": object(),
}
for k, v in sorted(d.items()):
        print(k, sys.getsizeof(v))