import pandas as pd
import matplotlib.pyplot as plt
import math

from pandas.core.algorithms import unique
# 11 import data
sell_data = pd.read_csv("uriage.csv")
customer_data = pd.read_excel("kokyaku_daicho.xlsx")
# pip install xlrd==1.2.0 で解決する
# print(sell_data.head())
# print(customer_data.head())

# 12 揺れの確認
# print(sell_data["item_name"].head())

# 13 クレンジングなしで集計
# 商品ごとの月売上合計
sell_data["purchase_date"] = pd.to_datetime(sell_data["purchase_date"])
sell_data["purchase_month"] = sell_data["purchase_date"].dt.strftime("%Y%m")
piv = pd.pivot_table(sell_data, index="purchase_month",
                     columns="item_name", aggfunc="size", fill_value=0)
# print(piv)

# 14 商品名のクレンジング
sell_data["item_name"] = sell_data["item_name"].str.upper()
sell_data["item_name"] = sell_data["item_name"].str.replace("  ", "")
sell_data["item_name"] = sell_data["item_name"].str.replace(" ", "")
result = sell_data.sort_values(by=["item_name"], ascending=True)
# print(result)
# Check
# print(len(pd.unique(sell_data["item_name"])) == 26)

# 15 NaNのクレンジング
# NaNの存在確認(axisは(x,y)=(0,1)?)
ch = sell_data.isnull().any(axis=0)
# print(ch)

# NaNをどのように補正するか？->今回は「商品単価の変動がない」ことを利用する
# 先にpriceを保持しておく方式に変更した(minmax実装は微妙な気がする)
price_dict = {}
for data in sell_data.sort_values(by=["item_name"], ascending=True).iterrows():
    if not math.isnan(data[1]["item_price"]):
        price_dict[data[1]["item_name"]] = data[1]["item_price"]

flg_is_null = sell_data["item_price"].isnull()

for data in list(sell_data.loc[flg_is_null, "item_name"].unique()):
    sell_data["item_price"].loc[(flg_is_null) & (
        sell_data["item_name"] == data)] = price_dict[data]

# 本の実装
# for trg in list(sell_data.loc[flg_is_null, "item_name"].unique()):
#     price = sell_data.loc[(~flg_is_null) & (
#         sell_data["item_name"] == trg), "item_price"].max()
#     sell_data["item_price"].loc[(fig_is_null) & (
#         sell_data["item_name"] == trg)] = price
# print(sell_data.head())

# 両者とも配列のコピーまわりでWarningが出る

# Check(Null)
# print(sell_data.isnull().any(axis=0))

# Check(補完が正しいか)
# for trg in list(sell_data["item_name"].sort_values().unique()):
#     print(trg+"の最大額:"+str(sell_data.loc[sell_data["item_name"] == trg]["item_price"].max()) +
#           "の最小額:"+str(sell_data.loc[sell_data["item_name"] == trg]["item_price"].min(skipna=False)))

# 16 顧客名の補正
# cust = customer_data["顧客名"].head()
# print(cust)
# print(sell_data["customer_name"].head())
customer_data["顧客名"] = customer_data["顧客名"].str.replace("　", "")
customer_data["顧客名"] = customer_data["顧客名"].str.replace(" ", "")
# print(customer_data["顧客名"].head())

# 17 日付の補正(tempt)
flg_is_serial = customer_data["登録日"].astype("str").str.isdigit()
print(flg_is_serial.sum())
