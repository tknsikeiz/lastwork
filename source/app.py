import sys
import msvcrt

products = {
    1: {"name": "特製ラーメン", "price": 1000, "sold": 0, "revenue": 0},
    2: {"name": "醤油ラーメン", "price": 780, "sold": 0, "revenue": 0},
    3: {"name": "しおラーメン", "price": 880, "sold": 0, "revenue": 0},
    4: {"name": "ごはん", "price": 150, "sold": 0, "revenue": 0}
}

cart = {}
total_revenue = 0

def display_title():
    print("***********************")
    print("    券売機シミュレータ   ")
    print("***********************")
    print("\nPlease Enter (Enterキー押下で画面がクリアされて処理が進む）")
    print("（ESCキー押下で管理画面に処理が進む）")
    print("（qキー押下でシミュレータ終了）")

def display_menu():
    print("\n商品      金額")
    print("=======================")
    for product_id, product in products.items():
        print(f"{product_id}. {product['name']} {product['price']}円")
    print("\n購入する商品番号(支払いに進む場合はc)>", end="")

def process_purchase():
    global cart, total_revenue
    total = 0
    while True:
        display_menu()
        user_input = input()

        if user_input == 'c':
            break

        if user_input.isdigit():
            product_id = int(user_input)
            if product_id in products:
                if product_id in cart:
                    cart[product_id] += 1
                else:
                    cart[product_id] = 1
                products[product_id]["sold"] += 1
                products[product_id]["revenue"] += products[product_id]["price"]
                total_revenue += products[product_id]["price"]
            else:
                print("商品番号またはcを指定してください。")
        else:
            print("商品番号またはcを指定してください。")

    print("\n商品       数量")
    print("=======================")
    for product_id, quantity in cart.items():
        print(f"{product_id}. {products[product_id]['name']} {quantity}個")
        total += products[product_id]['price'] * quantity

    print(f"===\n合計{total}円です。\n")
    return total

def process_payment(total):
    while True:
        print("現金を投入してください>", end="")
        try:
            money = int(input())
            if money <= 0:
                print("正の金額を投入してください。")
                return
            if money < total:
                print("金額が不足しています。")
                display_title()
                break
            else:
                change = money - total
                print(f"ご購入ありがとうございます。おつり{change}円です。")
                display_title()
                break
        except ValueError:
            print("無効な入力です。数字を入力してください。")

def management_screen(): 
    print("=== 管理メニュー ===")
    print("1. 売上をリセットする")
    print("2. 商品の価格を変更する")
    print("3. 管理画面を終了する")
    print("---")

def list_of_product(): 
    print("\n======= 商品一覧 =======")
    print('商品             単価 販売数 売上金額')
    print('=======================')
    for product_id, product in products.items():
        print(f'{product_id}. {product["name"]} {product["price"]}円     {product["sold"]}     {product["revenue"]}円')
    print('---')

def reset_sales():
    global total_revenue
    total_revenue = 0
    for product_id in products:
        products[product_id]["sold"] = 0
        products[product_id]["revenue"] = 0
    print("売上をリセットしました。\n")

def main():
    display_title()
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'q': 
                print("シミュレータを終了します。")
                sys.exit()
            elif key == b'\r': 
                cart.clear()
                total = process_purchase()
                if total > 0:
                    process_payment(total)
            elif key == b'\x1b':
                print("\n管理画面へ進みます...")
                list_of_product()
                while True:
                    management_screen()
                    management_input = input('管理コード入力: ')
                    if management_input.isdigit():  
                        management = int(management_input)
                        if management == 1:
                            reset_sales()
                            list_of_product()
                        elif management == 2:
                            if total_revenue == 0: 
                                list_of_product()
                                while True:
                                    product_input = input('価格を変更する商品の番号を入力してください。 >')
                                    if product_input.isdigit() and int(product_input) in products:
                                        product_number = int(product_input)
                                        change_amount = input('変更金額を入力してください。 >')
                                        if change_amount.isdigit():
                                            change_amount = int(change_amount)
                                            products[product_number]["price"] = change_amount
                                            print(f'【{products[product_number]["name"]}】の価格を{change_amount}円に変更しました。')
                                            list_of_product()
                                            break
                                        else:
                                            print('無効な金額です。再入力してください。')
                                    else:
                                        print('正しい商品番号を入力してください。')
                            else:
                                print('売上をリセットしてください。価格変更はリセット後に行えます。')
                        elif management == 3:
                            print("管理画面を終了します。")
                            display_title()
                            break
                        else:
                            print('無効な選択肢です。')
                    else:
                        print('無効な選択肢です。数字を入力してください。')
            else:
                print("無効なキーです。もう一度試してください。")

if __name__ == "__main__":
    main()

