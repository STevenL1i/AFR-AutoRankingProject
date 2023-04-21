import tkinter as tk

from screeninfo import get_monitors
reso = get_monitors()
reso_width = reso[0].width
reso_height = reso[0].height
window_width = 600
window_height = 400



window = tk.Tk()
window.title('AFR AutoRankingSystem v8.0')
window.geometry(f'{window_width}x{window_height}+{int(reso_width/2-window_width/2)}+{int(reso_height/2-window_height/2)}')
window.resizable(False, False)

testlabel1 = tk.Label(text="test label 1", font=("Arial", 18))
testlabel1.grid(row=0, column=0, padx=100, pady=100)
testlabel2 = tk.Label(text="test label 2")
testlabel2.grid(row=1, column=0)

window.mainloop()