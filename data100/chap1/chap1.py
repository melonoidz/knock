from pandas.plotting import scatter_matrix
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling as pdp
# 1 import and show data
customer_master = pd.read_csv('customer_master.csv')
# print(customer_data.head())

item_master = pd.read_csv('item_master.csv')

trans1_data = pd.read_csv('transaction_1.csv')
trans2_data = pd.read_csv('transaction_2.csv')
transdetail1_data = pd.read_csv('transaction_detail_1.csv')
transdetail2_data = pd.read_csv('transaction_detail_2.csv')

# 2 data union
transaction = pd.concat([trans1_data, trans2_data], ignore_index=True)
# print(str(len(trans1_data))+" "+str(len(trans2_data))+" "+str(len(transaction)))

transaction_detail = pd.concat(
    [transdetail1_data, transdetail2_data], ignore_index=True)

# file=pdp.ProfileReport(transaction_detail)
# file.to_file("data.html")
# 3 data join
join_data = pd.merge(transaction_detail, transaction[[
    "transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")
# transactionから必要なcolumnを指定し，onを軸にLeft Joinする(Appendix1参照)
# print(join_data.head())

# join_data_sub = pd.merge(transaction_detail, transaction[[
#                       "transaction_id", "customer_id"]], on="transaction_id", how="left")
# print(join_data_sub.head())

# 4 join data2(master)

join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
# print(join_data.head())

# 5 create column
# priceはLeft joinの影響で落ちるので再計算
join_data["price"] = join_data["quantity"] * join_data["item_price"]
# print(join_data[["quantity", "item_price", "price"]].head())

# 6 check data
# 元データのtransaction["price"], #5のpriceは一致するはず
check = (join_data["price"].sum() == transaction["price"].sum())
# print(check)

# 7 統計量の確認 ->1.NaNの状況把握, 2.全体の数字感
# print(join_data.isnull().sum())
# print(join_data.describe())

# 7 Appendix describeの可視化
# https://qiita.com/hik0107/items/de5785f680096df93efa

jd = join_data.describe()
# # 7.1 mean(平均値)
# plt.figure()
# jd[jd.index == "mean"].T.plot.bar(
#     yerr=jd[jd.index == "mean"].values, capsize=2)
# plt.savefig("mean.png")

# 7.2 四分位, minmax
plt.figure()
target = ["min", "25%", "50%", "75%", "max"]
jd[jd.index.isin(target)].boxplot()
plt.savefig("target.png")

# # 7.3 分布
# plt.figure()
# jd[jd.columns].plot(subplots=True, kind="kde")
# plt.savefig("kde.png")

# # 7.4 相関
# plt.figure()
# jd[jd.columns].corr().style.background_gradient(cmap="Oranges")
# plt.savefig("correspond.png")

# plt.figure()
# scatter_matrix(jd)
# plt.savefig("scatter.png")

# 8 時系列でデータを考察する
# print(join_data.dtypes)

# convert datetime
# datetimeへの変換
join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
# payment_monthの作成(strftimeで文字列として作成)
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")
# print(join_data[["payment_date", "payment_month"]].head())
# groupby
# print(join_data.groupby("payment_month").sum())

month_results = join_data.groupby("payment_month").sum()["price"]
plt.figure()
month_results.plot.bar()
# 微調整(https://qiita.com/Tatejimaru137/items/4ee6a73114d07d85bfd7)
plt.rcParams["font.size"] = 10
plt.tight_layout()

plt.title('month_results')
# plt.savefig("month_results.png")

# 9 月別・商品別データ集計
# print(join_data.groupby(["payment_month", "item_name"]).sum()[
#       ["price", "quantity"]])

# using pivot_table(row columnを指定できる)
# item_name, payment_month毎にデータを観察したい.
# Table形式はグラフに比べ推移が把握しにくい
piv = pd.pivot_table(join_data, index="item_name", columns="payment_month", values=[
                     "price", "quantity"], aggfunc="sum")
# print(piv)

# 10 Data Visualization
graph_data = pd.pivot_table(join_data, index="payment_month",
                            columns="item_name", values="price", aggfunc="sum")
print(graph_data.head())
plt.figure(figsize=(20, 20))
graph_data.plot()
# 良い感じにするやつ
plt.legend()
plt.savefig("result.png")
