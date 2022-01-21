import hashlib
import json
import datetime as dt

fooditemslist = []
orderslist = []
userdetialslist = []


def ReadFiles():
    try:
        with open('fooditemslist.txt', 'r') as fptr:
            data = fptr.readlines()
            for line in data:
                fooditemslist.append(json.loads(line.replace("'",'"')))


        with open('orderslist.txt', 'r') as fptr:
            data = fptr.readlines()
            for line in data:
                orderslist.append(json.loads(line.replace("'",'"')))

        with open('userdetialslist.txt', 'r') as fptr:
            data = fptr.readlines()
            for line in data:
                userdetialslist.append(json.loads(line.replace("'",'"')))
    except Exception as ex:
        error = ex

def upadatefiles():
    try:
        with open('fooditemslist.txt', 'w') as fptr:
            for line in fooditemslist:
                fptr.writelines(str(line) +"\n")

        with open('orderslist.txt', 'w') as fptr:
            for line in orderslist:
                fptr.writelines(str(line) +"\n")

        with open('userdetialslist.txt', 'w') as fptr:
            for line in userdetialslist:
                fptr.writelines(str(line) + "\n")

    except Exception as ex:
        print(ex.args)



def addFoodItem():
    name = input("Name: ")
    quantity = input("Quantity: ")
    price = input("Price: ")
    discount = input("Discount(%): ")
    stock = input("Stock: ")
    adminuser = Admin(name,quantity,price,discount,stock)


class Admin:

    def __init__(self,name,quantity,price,discount, stock):
        self.foodid = dt.datetime.now().strftime("%m%d%Y%H%M%S")
        fooditemslist.append({'foodid': self.foodid, 'name': name, 'quantity': quantity, 'price': price, 'discount': discount,
                          'stock': stock,'active':'True'})
        print("item added, Food Id :", self.foodid)

    def editfoodItem(foodid):
        edititem = None
        for item in fooditemslist:
            if item['foodid'] == foodid:
                edititem = item
                break
        if edititem is None:
            print(foodid, "not found")
        else:
            print(edititem)
            name = input("Updated Name: ")
            quantity = input("Updated Quantity: ")
            price = input("Updated Price: ")
            discount = input("Updated Discount(%): ")
            stock = input("Updated Stock: ")
            fooditemslist.remove(edititem)
            fooditemslist.append({'foodid': foodid, 'name': name, 'quantity': quantity, 'price': price, 'discount': discount,
                 'stock': stock,'active':'True'})
            print('item updated successfully')

    def viewAllFoodItems():
        for item in fooditemslist:
            if item['active'] == 'True':
                for key in item:
                  print(key,":",item[key])
        print('.................................')
    def deleteFoodItem(foodid):
        delitem = None
        for item in fooditemslist:
            if item['foodid'] == foodid:
                delitem = item
                break
        if delitem is None:
            print(foodid, "not found")
        else:
            fooditemslist.remove(delitem)
            delitem['active'] = 'False'
            fooditemslist.append(delitem)
            print(delitem['name'], "successfully deleted")


def adminfunctions():
    while True:
        print('1) Add new food item ')
        print('2) Edit food item ')
        print('3) View All food items ')
        print('4) Remove food item ')
        print("enter 0 to logout ")
        choose = int(input())
        if choose == 0:
            return
        elif choose == 1:
            addFoodItem()
        elif choose == 2:
            Admin.editfoodItem(input("enter food id: "))
        elif choose == 3:
            Admin.viewAllFoodItems()
        elif choose == 4:
            Admin.deleteFoodItem(input("enter food id: "))
        upadatefiles()




userid = None


def validateuser(loginusername, loginpassword):
    for user in userdetialslist:
        if user["loginusername"] == loginusername and user["loginpassword"] == loginpassword:
            global userid
            userid = user["userid"]
            return True
    return False


def createuser():
    loginusername = input("Full Name: ")
    mobile = input("Phone Number: ")
    email = input("Email: ")
    address = input("Address: ")
    loginpassword = input("password: ")
    repassword = input("Re-Enter password: ")
    while repassword != loginpassword:
        print("loginpassword Doesnt Match")
        loginpassword = input("password: ")
        repassword = input("Re-Enter password: ")

    user = User(loginusername,mobile,email,address,loginpassword)



def updatestock(foodids):
    for item in foodids:
        for food in fooditemslist:
            if food["foodid"] == item:
                food["stock"] = int(food["stock"]) - 1


def validatestock(orderlist,orderdic):
    seletedorders = {}
    for i in orderlist:
        for item in fooditemslist:
            if item['foodid'] == orderdic[i]:
                if item['foodid'] in seletedorders:
                    seletedorders[item['foodid']] += 1
                else:
                    seletedorders[item['foodid']] = 1
    for foodid in seletedorders:
        for item in fooditemslist:
            if item['foodid'] == foodid:
                if seletedorders[foodid] > int(item['stock']):
                    print('only',item['stock'],item['name'],'are available in stock')
                    print('you ordered',seletedorders[foodid])
                    print('please order again with value lesser than stock')
                    return False
    return True

class User:

    def __init__(self,loginusername,mobile,email,address,loginpassword,userid = None,update = False):
        if update:
            self.userid = userid
        else:
            self.userid = dt.datetime.now().strftime("%m%d%Y%H%M%S")
        res = hashlib.sha256(loginpassword.encode())
        loginpassword = res.hexdigest()

        userdetialslist.append({'userid': self.userid, 'loginusername': loginusername, 'mobile': mobile, 'email': email, 'address': address,
             'loginpassword': loginpassword})
        if update:
            print('updated successful')
        else:
            print("Account Created SuccessFully")
            print('use full Name for login username')


    def placeorder():
        n = 1
        orderdic = {}
        seletedorders = []
        for item in fooditemslist:
            if item['active'] == 'True' and int(item['stock']) > 0:
                print('%s)%s (%s) [INR %s]' % (n, item["name"], item["quantity"], item["price"]))
                orderdic[n] = item['foodid']
                n += 1
        if n == 1:
            print("No item is available to buy")
            return
        print('enter 0 to cancel')
        order = input("enter comma seperated order numbers, if multiple same orders then repeat order numbers: ")
        if order =='0':
            return
        orderlist = list(map(int, order.split(',')))
        if validatestock(orderlist,orderdic) == False:
            return
        print("selected orders are :- ")
        totalamount = 0
        n = 1
        for i in orderlist:
            for item in fooditemslist:
                if item['foodid'] == orderdic[i]:
                    print('%s)%s (%s) [%s]' % (n, item["name"], item["quantity"], item["price"]))
                    n += 1
                    seletedorders.append(item['foodid'])
                    totalamount += int(item["price"]) - int(item["price"]) * float(item['discount']) / 100
                    break
        print('Total Amount after discount:', totalamount)
        orderconfirm = int(input("enter 1 to confirm order, 0 to cancel: "))
        if orderconfirm == 1:
            updatestock(seletedorders)
            orderslist.append({'userid': userid, 'orderslist': seletedorders, 'datetime': str(dt.datetime.now())})
            print("order placed")

    def gerorderhistory(userid):
        noordersplaced = True
        for val in orderslist:
            orderedtime = None
            orderidcount = {}
            if val['userid'] == userid:
                orderedtime = val['datetime']

                for item in val['orderslist']:
                    if item in orderidcount:
                        orderidcount[item] += 1
                    else:
                        orderidcount[item] = 1
                        noordersplaced = False

            i = 1
            if orderedtime == None:
                continue
            print('ordered on:', orderedtime)
            for order in orderidcount:
                for item in fooditemslist:
                    if item['foodid'] == order:
                        sno = str(i) + ')'
                        print(sno, item['name'], 'X', orderidcount[order])
                        i += 1

        if noordersplaced:
            print('no orders placed yet')
        print("\n\n")


def updateuser(userid):
    loginusername = input("Full Name: ")
    mobile = input("Phone Number: ")
    email = input("Email: ")
    address = input("Address: ")
    loginpassword = input("password: ")
    repassword = input("Re-Enter password: ")
    while repassword != loginpassword:
        print("password Doesnt Match")
        loginpassword = input("password: ")
        repassword = input("Re-Enter password: ")
    tempuser = None
    for user in userdetialslist:
        if user['userid'] == userid:
            tempuser = user
            break
    userdetialslist.remove(tempuser)
    user = User(loginusername, mobile, email, address, loginpassword, userid=userid,update=True)
    print("profile updated")

def userfunctions():
    while True:
        upadatefiles()
        print('1) Place New Order')
        print('2) Order History')
        print('3) Update Profile')
        print("enter 0 to logout ")
        try:
            choose = int(input())
            if choose == 1:
                User.placeorder()
            if choose == 2:
                User.gerorderhistory(userid)
            if choose == 3:
                updateuser(userid)
            upadatefiles()
            if choose == 0:
                return
        except:
            print("enter valid values")


adminusername = 'admin'
adminpassword = '7676aaafb027c825bd9abab78b234070e702752f625b752e55e55b48e607e358'


def login():
    if loginusername == adminusername and loginpassword == adminpassword:
        return True
    elif validateuser(loginusername, loginpassword):
        return True
    return False



ReadFiles()
while True:
    try:
        upadatefiles()
        option = int(input("Enter 1 to login, 2 to Create new user, enter 0 to exit the application: "))
        if option not in [0, 1, 2]:
            raise ("please enter only 0,1,2")
        if option == 0:
            break
        elif option == 2:
            createuser()
        elif option == 1:
            loginusername = input("Enter username: ")
            res = hashlib.sha256(input("Enter password: ").encode())
            loginpassword = res.hexdigest()
            if login():
                while True:
                    print("Welcome",loginusername)
                    if loginusername == adminusername:
                        adminfunctions()
                    else:
                        userfunctions()
                    break
            else:
                print("Log in Failed")

    except:
        print("please enter only 0,1,2")
