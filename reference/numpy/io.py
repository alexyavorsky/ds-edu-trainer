# Примеры к статье numpy/io.
# Каждый пример выполняется в своей временной папке, поэтому файлы можно создавать свободно.

# %% setup
scores = np.array([[4.5, 3.0, 5.0],
                   [3.5, 4.0, 4.5]])

# %% npy
np.save("scores.npy", scores)            # двоичный формат NumPy: тип и форма сохраняются
np.load("scores.npy")
# ─── вывод ───
# array([[4.5, 3. , 5. ],
#        [3.5, 4. , 4.5]])

# %% npz
np.savez("data.npz", scores=scores, ids=np.array([101, 102]))
data = np.load("data.npz")
print(data.files)
data["ids"]
# ─── вывод ───
# ['scores', 'ids']
# array([101, 102])

# %% txt
np.savetxt("scores.csv", scores, delimiter=",", fmt="%.1f", header="math,phys,chem")
with open("scores.csv") as f:
    print(f.read())
np.loadtxt("scores.csv", delimiter=",")  # строка заголовка начинается с # и пропускается
# ─── вывод ───
# # math,phys,chem
# 4.5,3.0,5.0
# 3.5,4.0,4.5
#
# array([[4.5, 3. , 5. ],
#        [3.5, 4. , 4.5]])

# %% loadtxt-cols
with open("prices.csv", "w") as f:
    f.write("id,price,qty\n1,120.5,3\n2,80.0,10\n")
np.loadtxt("prices.csv", delimiter=",", skiprows=1, usecols=(1, 2))
# ─── вывод ───
# array([[120.5,   3. ],
#        [ 80. ,  10. ]])

# %% genfromtxt
with open("temps.csv", "w") as f:
    f.write("day,temp\n1,12.5\n2,\n3,14.0\n")
np.genfromtxt("temps.csv", delimiter=",", skip_header=1)   # пустое поле → nan
# ─── вывод ───
# array([[ 1. , 12.5],
#        [ 2. ,  nan],
#        [ 3. , 14. ]])

# %% loadtxt-missing [raises=ValueError]
with open("temps.csv", "w") as f:
    f.write("1,12.5\n2,\n3,14.0\n")
np.loadtxt("temps.csv", delimiter=",")
# ─── вывод ───
# ValueError: could not convert string '' to float64 at row 1, column 2.

# %% pickle [raises=ValueError]
records = np.array([{"id": 1}, None], dtype=object)   # массив объектов Python
np.save("records.npy", records)                        # сохраняется через pickle
np.load("records.npy")
# ─── вывод ───
# ValueError: Object arrays cannot be loaded when allow_pickle=False
