import items

cart = {}


def addItem(item, quantity):
    if item in cart:
        cart[item] += quantity
    else:
        cart[item] = quantity


def decrementItem(item, quantity):
    if item in cart:
        cart[item] -= quantity

        for item, quantity in cart.items():
            if quantity <= 0:
                removeItem(item)
                return


def removeItem(item):
    if item in cart:
        del cart[item]


def calculateCost():
    cost = 0.00

    for i in range(len(items.items)):
        cost += items.items[i]['price'] * getItemQuantity(items.items[i]['name'])

    return cost


def getItemQuantity(i):
    if i in cart:
        for item, quantity in cart.items():
            if i == item:
                return quantity
    return 0
