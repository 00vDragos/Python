class MathService:
    def __init__(self):
        self.cache = {
            "pow": {},
            "factorial": {},
            "fib": {}
        }

    def pow(self, base: float, exponent: float) -> tuple[float, bool]:
        key = (base, exponent)
        if key in self.cache["pow"]:
            print(f"[CACHE HIT] pow{key} = {self.cache['pow'][key]}")
            return self.cache["pow"][key], True

        print(f"[CACHE MISS] Calculam pow pentru {key}...")
        result = base ** exponent
        self.cache["pow"][key] = result
        return result, False

    def factorial(self, n: int) -> tuple[int, bool]:
        if n < 0:
            raise ValueError("n must be >= 0")

        if n in self.cache["factorial"]:
            print(f"[CACHE HIT] factorial({n}) = {self.cache['factorial'][n]}")
            return self.cache["factorial"][n], True

        print(f"[CACHE MISS] Calculam factorial pentru {n}...")
        result = 1
        for i in range(2, n + 1):
            result *= i

        self.cache["factorial"][n] = result
        return result, False

    def fib(self, n: int) -> tuple[int, bool]:
        if n < 0:
            raise ValueError("n must be >= 0")

        if n in self.cache["fib"]:
            print(f"[CACHE HIT] fib({n}) = {self.cache['fib'][n]}")
            return self.cache["fib"][n], True

        print(f"[CACHE MISS] Calculam fibonacci pentru {n}...")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b

        self.cache["fib"][n] = a
        return a, False
