import sys
import importlib.metadata

DEPENDENCIES = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
    "requests": "Network access ready",
}
missing_package = []
for pkg in DEPENDENCIES:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Missing package {pkg}")
        missing_package.append(pkg)
        

if missing_package:
    print(
        "Packages missing!\n"
        "Use 'pip install -r requirements.txt' or "
        "'poetry install' to instal missing packages"
        )
    sys.exit(1)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def check_versions() -> dict[str, str]:
    versions = {}
    for pkg in DEPENDENCIES:
        try:
            versions[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            versions[pkg] = "Unknown"
    return versions

def matrix_data() -> None:
    rolls = np.random.randint(1, 7, size = 100)
    results = np.arange(1, 101)
    data_frame = pd.DataFrame({"res": results, "roll": rolls})
    plt.figure()
    plt.plot(data_frame["res"], data_frame["roll"], marker = "o")
    plt.title("Dice Rolls")
    
    plt.savefig("dice_result.png")
    plt.show()
    plt.close()

if __name__ == "__main__":
    
    check_versions()
    matrix_data()







#NumPy arrays are stored at one continuous 
# place in memory unlike lists, so processes can
# access and manipulate them very efficiently.
# class Dice:
#     def __init__(self, num_sides = 6) -> None:
#         self.num_sides = num_sides

#     def roll(self) -> int:
#         return random.randint(1, self.num_sides)

#generate 1000 random dice result
# results = random.randint(6, size = (1000))
# dice = Dice()
# results = []
# for _ in range(1000):
#     res = dice.roll()
#     results.append(res)

# print(results)
# plt.hist(results, bins=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5], rwidth=0.8)
# plt.title("Dice Rolls")
# plt.show()
# plt.savefig("dice_result.png")
# plt.close()

