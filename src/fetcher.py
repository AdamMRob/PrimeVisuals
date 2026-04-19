import re
import requests

# First 10,000 primes published by the University of Tennessee prime pages
_SOURCE_URL = "https://primes.utm.edu/lists/small/10000.txt"

_cache: list[int] | None = None


def fetch_primes(limit: int = 10_000) -> list[int]:
    global _cache
    if _cache is None:
        print("Fetching primes from primes.utm.edu ...")
        response = requests.get(_SOURCE_URL, timeout=10)
        response.raise_for_status()
        _cache = [int(n) for n in re.findall(r"\d+", response.text)]
        # The file contains a count header; remove any non-prime leading numbers
        # The first prime is 2, so trim anything before it
        start = next(i for i, v in enumerate(_cache) if v == 2)
        _cache = _cache[start:]
    return _cache[:limit]
