# Примеры к статье sample/classes (образец платформы).
# Вывод под примерами пишет scripts/validate_reference.py --update — руками не править.

# %% setup
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def __repr__(self):
        return f"Counter(value={self.value})"

# %% two-counters
a, b = Counter(), Counter()
a.increment()
a.increment()
b.increment()
print(a.value, b.value)
# ─── вывод ───
# 2 1

# %% repr
c = Counter()
c.increment()
c
# ─── вывод ───
# Counter(value=1)

# %% no-self [raises=TypeError]
class Broken:
    def ping():
        return "pong"

Broken().ping()
# ─── вывод ───
# TypeError: Broken.ping() takes 0 positional arguments but 1 was given

