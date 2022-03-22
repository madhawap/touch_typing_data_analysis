# import matplotlib.pyplot as plt
# https://matplotlib.org/stable/tutorials/introductory/pyplot.html

records = []
typingSpeed = []
days = []
accuracy = []

with open("touchTypingProgress.csv", "r") as file:
    for line in file:
        records.append(line.strip())

for record in records[1:]:
    if record != "":
        typingSpeed.append(int(record.split(",")[1]))
    days.append(record.split(",")[0])
    if record.split(",")[3] != "":
        accuracy.append(float(record.split(",")[3]))

# plt.plot(typingSpeed)
# plt.ylabel('some numbers')
# plt.show()

print(f'Total tests taken \033[95m {len(records)} \033[0m')
print(f'Total hours spent \033[95m {len(records) / 60}h \033[0m')
print(f'Avg typing speed is \033[95m {sum(typingSpeed) / len(typingSpeed)} \033[0m')
print(f'Avg accuracy is \033[95m {sum(accuracy) / len(accuracy)} \033[0m')
