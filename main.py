from tkinter import messagebox, ttk
import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import webbrowser

#window settings
window = tk.Tk()
window.title("Expense Tracker")
window.geometry("900x600")
window.resizable(width=False, height=False)

#error window
def errorWindow(valueOfError):
    messagebox.showerror('Error', valueOfError)

#main label
mainlabel = tk.Label(window, text = "Insert your expenses", font = ('Arial', 18))
mainlabel.pack(padx=20, pady=20)

#sum label
sumlabel = tk.Label(window, text=f'Sum: 0 $', font=('Arial', 10))
sumlabel.place(relx=0.4, rely=0.6)

#link button
def callback():
    webbrowser.open(r"https://www.linkedin.com/in/filip-pawlicki-0b0891283/")

link = tk.Button(window, text="My LinkedIn", command=callback, font=('Arial', 18))
link.place(relx=0.4, rely=0.7)

#frame for chart
frame = tk.Frame(window, width=100, height=100)
frame.place(relx=0.6, rely=0.2)

#appending expenses to TreeView
def can_convert_to_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

costPerCategory={}
def append_expenses():
    if nameOfExpense.get() == '':
        errorWindow('Please enter a name of your expense')
    elif value_category.get() == "Select a category":
        errorWindow('Please select a category')
    elif priceOfExpense.get() == '' or not can_convert_to_float(priceOfExpense.get()):
        errorWindow('Please enter a price of your expense')
    else:
        listOfExpenses.insert(parent='', index='end', text=str(len(listOfExpenses.get_children())+1), values=[nameOfExpense.get(), value_category.get(), str(priceOfExpense.get())+' $'])
        nameOfExpense.delete(0, tk.END)
        value_category.set("Select a category")
        priceOfExpense.delete(0, tk.END)

        #summarizing cost of all expenses
        prices = []

        for child in listOfExpenses.get_children():
            prices.append(float(listOfExpenses.item(child)["values"][2][0:-2]))
            if listOfExpenses.item(child)["values"][1] in costPerCategory:
                costPerCategory[listOfExpenses.item(child)["values"][1]] += float(listOfExpenses.item(child)["values"][2][0:-2])
            else:
                costPerCategory[listOfExpenses.item(child)["values"][1]] = float(listOfExpenses.item(child)["values"][2][0:-2])

        total=sum(prices)
        sumlabel = tk.Label(window, text=f'Sum: {total} $', font=('Arial', 10))
        sumlabel.place(relx=0.4, rely=0.6)
        for widgets in frame.winfo_children():
            widgets.destroy()
        pieChart()

#adding expenses
categories = ['Food', 'Transport', 'Personal', 'Housing']

namelabel = tk.Label(window, text='Enter a name', font=('Arial', 10))
namelabel.place(relx=0.05, rely=0.1)

nameOfExpense = tk.Entry(window, width=50)
nameOfExpense.place(relx=0.05, rely=0.15, anchor=tk.W)

value_category = tk.StringVar(window)
value_category.set("Select a category")
categoryMenu = tk.OptionMenu(window, value_category, *categories)
categoryMenu.place(relx=0.4, rely=0.15, anchor=tk.W)

pricelabel = tk.Label(window, text='Enter a price', font=('Arial', 10))
pricelabel.place(relx=0.57, rely=0.1)

priceOfExpense = tk.Entry(window, width=10)
priceOfExpense.place(relx=0.57, rely=0.15, anchor=tk.W)

submit_button = tk.Button(window, text='Add', command=append_expenses)
submit_button.place(relx=0.67, rely=0.15, anchor=tk.W)

#TreeView of all expenses
listOfExpenses = ttk.Treeview(window)
listOfExpenses.place(relx=0.05, rely=0.2, width= 400)
listOfExpenses['columns'] = ("Name", "Category", "Price")

listOfExpenses.column("#0", width=5, anchor=tk.W)
listOfExpenses.column("Name", anchor=tk.CENTER, width= 200)
listOfExpenses.column("Category", anchor=tk.CENTER, width=17)
listOfExpenses.column("Price", anchor=tk.E,width=15)

listOfExpenses.heading('#0', text='ID')
listOfExpenses.heading('Name', text='Name')
listOfExpenses.heading('Category', text='Category')
listOfExpenses.heading('Price', text='Price')

#locking sizing of columns by user
def handle_click(event):
    if listOfExpenses.identify_region(event.x, event.y) == "separator":
        return "break"

listOfExpenses.bind('<Button-1>', handle_click)

#pie chart of expenses by category
def pieChart():
    y = np.array(list(costPerCategory.values()))
    mylabels = list(costPerCategory.keys())

    f=Figure(figsize=(3,3))
    ax = f.add_subplot(111)
    ax.pie(y, radius=1, autopct='%0.2f%%')
    ax.legend(mylabels, loc='upper right', fontsize=7, bbox_to_anchor=(1.1, 1.1))
    canvas = FigureCanvasTkAgg(f, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()



window.mainloop()


