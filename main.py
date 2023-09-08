import threading
import time
from tkinter import *

from PIL import Image, ImageTk

import items
import order

resturantName = 'Muriale\'s Italian Kitchen'
appName = f'{resturantName}\'s Grocery Ordering System'
backgroundColor = '#E9CBA7'

nameFont = ("Helvetica", 10, "bold")
itemFont = ("Verdana", 10)
buttonFont = ("Verdana", 15)
titleFont = ('Arial', 20)

root = Tk()
x = 1250
y = 1000
root.title(appName)
root.geometry(f'{x}x{y}')
root.configure(bg=backgroundColor)

imageWidth = 50
imageHeight = 50

headerFrame = Frame(root, bg=backgroundColor)

# restaurant name and app name
resturantLabel = (Label(headerFrame, text=resturantName, font=titleFont, bg=backgroundColor))
resturantLabel.place(x=x / 2 - 150, y=10)

Label(headerFrame, text=appName, font=titleFont, bg=backgroundColor).place(x=x / 2 - 300, y=50)

itemsFrame = Frame(root, bg=backgroundColor)

exitFlag = False

images = []

for i in range(len(items.items)):
    images.append(ImageTk.PhotoImage(Image.open(items.items[i]['image']).resize((imageWidth, imageHeight))))


def showItems():
    global exitFlag
    exitFlag = False

    for i in range(10):
        name = items.items[i]['name']
        Label(itemsFrame, text=items.items[i]['name'], font=itemFont, bg=backgroundColor).grid(row=i, column=1)
        Label(itemsFrame, image=images[i], bg=backgroundColor).grid(row=i, column=2, padx=10, pady=15)
        Label(itemsFrame, text=items.items[i]['description'], font=itemFont, bg=backgroundColor).grid(row=i, column=3,
                                                                                                      padx=10)
        Label(itemsFrame, text=f'${items.items[i]["price"]}', font=itemFont, bg=backgroundColor).grid(row=i, column=4,
                                                                                                      padx=10)
        Label(itemsFrame, text=f"x{order.getItemQuantity(name)}", font=itemFont, bg=backgroundColor).grid(row=i,
                                                                                                          column=5,
                                                                                                          padx=10)
        Button(itemsFrame, text='+', font=buttonFont, command=lambda i=i, name=name: order.addItem(name, 1),
               bg=backgroundColor).grid(row=i, column=6)
        Button(itemsFrame, text='−', font=buttonFont, command=lambda i=i, name=name: order.decrementItem(name, 1),
               bg=backgroundColor).grid(row=i,
                                        column=7)
        itemsFrame.pack()

    for i in range(10, 20):
        name = items.items[i]['name']
        Label(itemsFrame, text=items.items[i]['name'], font=itemFont, bg=backgroundColor).grid(row=i - 10, column=8)
        Label(itemsFrame, image=images[i], bg=backgroundColor).grid(row=i - 10, column=9, padx=10, pady=15)
        Label(itemsFrame, text=items.items[i]['description'], font=itemFont, bg=backgroundColor).grid(row=i - 10,
                                                                                                      column=10,
                                                                                                      padx=10)
        Label(itemsFrame, text=f'${items.items[i]["price"]}', font=itemFont, bg=backgroundColor).grid(row=i - 10,
                                                                                                      column=11,
                                                                                                      padx=10)
        Label(itemsFrame, text=f"x{order.getItemQuantity(name)}", font=itemFont, bg=backgroundColor).grid(row=i - 10,
                                                                                                          column=12,
                                                                                                          padx=10)
        Button(itemsFrame, text='+', font=buttonFont, command=lambda i=i, name=name: order.addItem(name, 1),
               bg=backgroundColor).grid(row=i - 10, column=13)
        Button(itemsFrame, text='−', font=buttonFont, command=lambda i=i, name=name: order.decrementItem(name, 1),
               bg=backgroundColor).grid(row=i - 10,
                                        column=14)
        itemsFrame.pack()


def updateQuantities():
    while not exitFlag:
        for i in range(10):
            Label(itemsFrame, text=f"x{order.getItemQuantity(items.items[i]['name'])}", font=itemFont,
                  bg=backgroundColor).grid(row=i, column=5)
        for i in range(10, 20):
            Label(itemsFrame, text=f"x{order.getItemQuantity(items.items[i]['name'])}", font=itemFont,
                  bg=backgroundColor).grid(row=i - 10, column=12)

        # total
        Label(headerFrame, text=f'Total: ${order.calculateCost():.2f}', font=itemFont, bg=backgroundColor).grid(
            column=1, row=2,
            padx=1000)
        itemsFrame.pack()
        headerFrame.pack()
        time.sleep(0.25)


thread = threading.Thread(target=updateQuantities)
thread.start()


def checkout():
    global exitFlag
    exitFlag = True

    for i in itemsFrame.winfo_children():
        i.grid_forget()

    def thankYou():
        for i in itemsFrame.winfo_children():
            i.grid_forget()

        Label(itemsFrame, text='Thank you for your order!', font=titleFont, bg=backgroundColor).grid(row=0, column=1,
                                                                                                     padx=30, pady=50)
        Button(itemsFrame, text='Finish', bg=backgroundColor, font=buttonFont, command=cancel).grid(row=1, column=1,
                                                                                                    padx=30, pady=50)
        itemsFrame.pack()

    def cancel():
        for i in itemsFrame.winfo_children():
            i.grid_forget()

        global exitFlag
        exitFlag = False
        thread = threading.Thread(target=updateQuantities)
        thread.start()
        order.cart.clear()
        showItems()
        itemsFrame.pack()

    Button(itemsFrame, text='Place Order', font=buttonFont, command=thankYou, bg=backgroundColor).grid(row=0, column=1,
                                                                                                       padx=30, pady=50)
    Button(itemsFrame, text='Cancel Order', font=buttonFont, command=cancel, bg=backgroundColor).grid(row=0, column=3,
                                                                                                      padx=30, pady=50)

    for item, quantity in order.cart.items():
        if quantity <= 0:
            continue
        Label(itemsFrame, text='Special Requests:', font=nameFont, bg=backgroundColor).grid(row=0, column=4, padx=10, pady=10)
        for i in range(len(items.items)):
            if item == items.items[i]['name']:
                Label(itemsFrame, text=f"Item: {item}", bg=backgroundColor).grid(row=i + 1, column=1, padx=10, pady=10)
                Label(itemsFrame, text=f"Quantity: {quantity}", bg=backgroundColor).grid(row=i + 1, column=2, padx=10,
                                                                                         pady=10)
                Label(itemsFrame, text=f"Cost: ${str(quantity * items.items[i]['price'])}", bg=backgroundColor).grid(
                    row=i + 1, column=3)
                Text(itemsFrame, height=2, width=30).grid(row=i + 1, column=4)
            i += 1

    # total
    Label(itemsFrame, text=f'Total: ${order.calculateCost():.2f}', font=buttonFont, bg=backgroundColor).grid(
        row=len(items.items),
        column=2)
    itemsFrame.pack()


# checkout button
Button(headerFrame, text='Checkout', font=buttonFont, command=checkout, bg=backgroundColor).grid(column=1, row=1,
                                                                                                 padx=1000, pady=15)

headerFrame.pack()

showItems()

root.mainloop()
