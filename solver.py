import tkinter as tk
from tkinter.constants import ACTIVE, BOTH, BOTTOM, CENTER, DISABLED, FLAT, LEFT, RAISED, RIGHT, SUNKEN, TOP

f = open("words_alpha.txt", "r")
words = f.read().splitlines()
letter_counts = []
for i in range(0, len(words)):
    letter_counts.append([0] * 26)

for i in range(0, len(words)):
    for c in words[i]:
        letter_counts[i][ord(c) - ord('a')] += 1


def solve(anagram):
    letter_count = [0] * 26
    for c in anagram:
        letter_count[ord(c) - ord('a')] += 1
    res = []
    for i in range(0, len(words)):
        if all(map(lambda x: letter_count[x] >= letter_counts[i][x], range(0, 26))):
            res.append(words[i])
    res.sort(key = str.__len__, reverse = True)
    return res

# def printFirst(list, cnt):
#     for i in range(0, min(len(list), cnt)):
#         print(list[i])

# while (True):
#     try:
#         anagram, cnt = input().split()
#     except (ValueError):
#         continue
#     except (EOFError):
#         break
#     cnt = int(cnt)
#     printFirst(solve(anagram), cnt)


window = tk.Tk()
window.title("Anagram Cheater")

renderedLabels = []
anagramResults = []
currentStartIndex = 0
maxOnePage = 15    # number of results on 1 page

def clear_rendered_labels():
    for label in renderedLabels:
        label.destroy()

def render(startIndex, renderAmount):
    for i in range(0, renderAmount):
        if (startIndex + i >= len(anagramResults)):
            break
        renderedLabels.append(tk.Label(
            master = resultFrame,
            font = ("Courier", 15),
            text = anagramResults[startIndex + i]
        ))
        renderedLabels[-1].pack()

def disable_button(button):
    button["cursor"] = "arrow"
    button["state"] = "disabled"

def enableButton(button):
    button["cursor"] = "hand2"
    button["state"] = "normal"

def isButtonDisabled(button):
    return button["state"] == "disabled"

def updateButtonAvailability():
    if (currentStartIndex == 0):
        disable_button(previousPageButton)
    else:
        if isButtonDisabled(previousPageButton):
            enableButton(previousPageButton)

    if (currentStartIndex + maxOnePage >= len(anagramResults)):
        disable_button(nextPageButton)
    else:
        if (isButtonDisabled(nextPageButton)):
            enableButton(nextPageButton)


def process():
    clear_rendered_labels()
    anagram = anagramEntry.get().lower()
    global anagramResults
    anagramResults = solve(anagram)
    currentStartIndex = 0
    render(currentStartIndex, maxOnePage)
    updateButtonAvailability()

def nextPage():
    global currentStartIndex
    currentStartIndex += maxOnePage
    clear_rendered_labels()
    render(currentStartIndex, maxOnePage)
    updateButtonAvailability()

def previousPage():
    global currentStartIndex
    currentStartIndex -= maxOnePage
    clear_rendered_labels()
    render(currentStartIndex, maxOnePage)
    updateButtonAvailability()


titleFrame = tk.Frame()
title = tk.Label(
    master = titleFrame,
    text = "Anagram Cheater",
    fg = "white",
    bg = "#656565",
    font = ("Courier", 30, "bold"),
    relief = RAISED
)
title.pack()  

anagramEntryFrame = tk.Frame(
    bg = "lightgrey",
)
anagramEntry = tk.Entry(
    master = anagramEntryFrame,
    bg = "lightgrey",
    font = ("Courier", 20),
    justify = CENTER,
    relief = FLAT
)
anagramEntry.pack(padx = 5, pady = 5)

# numberEntryFrame = tk.Frame()
# numberEntry = tk.Entry(
#     master = numberEntryFrame,
#     bg = "lightgrey",
#     font = ("Courier", 20)
# )
# numberEntryFrame.grid(row = 1, column = 1)
# numberEntry.pack()

buttonFrame = tk.Frame()
button = tk.Button(
    master = buttonFrame,
    font = ("Courier", 20, "bold"),
    text = "Solve!",
    bg = "#656565",
    fg = "white",
    cursor = "hand2",
    command = process
)
button.pack()

titleFrame.grid(row = 0, column = 0, padx = 5, pady = 5)
anagramEntryFrame.grid(row = 1, column = 0)
buttonFrame.grid(row = 2, column = 0, padx = 5, pady = 5)

resultFrame = tk.Frame()
resultFrame.grid(row = 3, column = 0, pady = 10)

nextPageFrame = tk.Frame()
previousPageFrame = tk.Frame()
nextPageButton = tk.Button(
    master = nextPageFrame,
    font = ("Courier", 20, "bold"),
    fg = "white",
    bg = "#656565",
    text = "Next page",
    state = DISABLED,
    command = nextPage
)

previousPageButton = tk.Button(
    master = previousPageFrame,
    font = ("Courier", 20, "bold"),
    fg = "white",
    bg = "#656565",
    text = "Previous page",
    state = DISABLED,
    command = previousPage
)
nextPageFrame.grid(row = 1, column = 1)
previousPageFrame.grid(row = 2, column = 1)
nextPageButton.pack()
previousPageButton.pack()

window.mainloop()