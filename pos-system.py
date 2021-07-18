import os
import sys
from datetime import datetime

import pandas as pd

datetime_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
READ_CSV_PATH = os.path.join(os.getcwd(), "csv/product_master.csv")
RECEIPT_PATH = os.path.join(os.getcwd(), f"receipt/{datetime_now}.txt")


# 商品クラス
class Item:
    def __init__(self, item_code: str, item_name: str, price: int):
        self.item_code: str = item_code
        self.item_name: str = item_name
        self.price: int = price

    def get_price(self):
        return self.price


# オーダークラス
class Order:
    def __init__(self, item_master):
        self.item_order_list = []
        self.item_count_list = []
        self.item_master = item_master

    def fetch_item_data(self, item_code: str):
        for item in self.item_master:
            if item.item_code == item_code:
                item_data = {
                    "item_code": item.item_code,
                    "item_name": item.item_name,
                    "price": item.price,
                }
                return item_data

    def add_item_order_list(self, item_code: str, item_count: int):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
        print("買い物かごに追加しました。")

    def input_order(self):
        while True:
            # 商品コード入力
            order_item_code: str = input("注文したい商品コードを入力してください。未入力で注文処理へ。>>")
            order_item_code = order_item_code.strip()
            if order_item_code.strip():
                if self.item_exists(order_item_code):
                    # 数量入力
                    while True:
                        order_item_count: str = input("数量を入力してください。>>")
                        order_item_count = order_item_count.strip()
                        try:
                            order_item_count_int: int = int(order_item_count)
                            break
                        except Exception:
                            print("数量を正しく入力してください。")
                            pass
                    # オーダーリストに追加
                    self.add_item_order_list(order_item_code, order_item_count_int)
                else:
                    print("商品コードに誤りがあります。")
                    continue
            else:
                print("清算処理へ移ります。")
                break

    def item_exists(self, order_item_code: str):
        for item in self.item_master:
            if item.item_code == order_item_code:
                return True
        return False

    def add_item_order(self, item_code: str):
        self.item_order_list.append(item_code)

    def view_item_list(self):
        total_price: int = 0
        for order_item_code, order_count in zip(
            self.item_order_list, self.item_count_list
        ):
            item_data = self.fetch_item_data(order_item_code)
            item_total_price: int = int(item_data["price"]) * int(order_count)
            self.write_receipt("商品コード：{}".format(item_data["item_code"]))
            self.write_receipt("商品名：{}".format(item_data["item_name"]))
            self.write_receipt("金額：{}".format("{:,}".format(item_data["price"])))
            self.write_receipt("数量：{}".format("{:,}".format(order_count)))
            self.write_receipt("小計：￥{}円".format("{:,}".format(item_total_price)))
            self.write_receipt("===================================")
            total_price += item_total_price
        self.write_receipt("合計：￥{}円".format("{:,}".format(total_price)))
        print("合計：￥{}円になります。".format("{:,}".format(total_price)))
        # 精算処理
        self.pay_off(total_price)
        print("レシートが発行されました。")
        print("ありがとうございました。")

    def write_receipt(self, write_text: str):
        with open(
            RECEIPT_PATH,
            mode="a",
            encoding="utf_8_sig",
        ) as f:
            f.write(write_text + "\n")

    def pay_off(self, total_price: int):
        while True:
            pay_price_str: str = input("支払い金額を入力してください>>")
            pay_price_str = pay_price_str.strip()
            try:
                pay_price: int = int(pay_price_str)
                if total_price <= pay_price:
                    break
                else:
                    print("料金が不足しています。")
                    pass
            except Exception:
                print("金額を正しく入力してください。")
                pass
        change_price: int = pay_price - total_price
        self.write_receipt("預かり金額：￥{}円".format("{:,}".format(pay_price)))
        self.write_receipt("おつり：￥{}円".format("{:,}".format(change_price)))
        if change_price > 0:
            print("{}円のお返しになります。".format("{:,}".format(change_price)))


# メイン処理
def main():
    item_master = reegist_master()
    # 商品一覧表示
    for item in item_master:
        print(f"{item.item_code} {item.item_name} {item.price}")
    # オーダー登録
    order = Order(item_master)
    order.input_order()
    # オーダー表示
    order.view_item_list()


def reegist_master():
    item_master = []
    try:
        df = pd.read_csv(
            READ_CSV_PATH, dtype={"item_code": object, "item_name": object}
        )
        for index, row in df.iterrows():
            # マスタ登録
            item_master.append(
                Item(row["item_code"], row["item_name"], int(row["price"]))
            )
        return item_master
    except Exception:
        print("マスタ登録できませんでした。")
        sys.exit()


if __name__ == "__main__":
    main()
