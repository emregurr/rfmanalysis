import pandas as pd

import numpy as np

import datetime as dt

retail = pd.read_excel(r"C:\Users\acer\Desktop\Module\3\online_retail_II.xlsx", sheet_name="Year 2010-2011")

df = retail.copy()

df.head()

df.shape

df.info()

# Data'da Herhangi bir eksik değer var mı ?
df.isnull().values.any()

# Degiskenlerde kaç tane eksik değer var ?
df.isnull().sum()

# Degiskenlerde ki toplam eksik değer sayısı ?
df.isnull().sum().sum()

# Eksik değerlerin tüm Data'ya oranı nedir ?
print("%.2f" % (df.isnull().sum().sum() / df.shape[0]))

# 541910 gözlem var , 25900 eşsiz fatura numarası var.Bir fatura numarasından kaç satır var ?
df["Invoice"].nunique()

# Ornegin fatura numarası 536365 olan 7 satır var , her bir yeni ürün girişinde aynı fatura numarası ile yeni satır olusmus
df[df["Invoice"] == 536365]

# Veri setinde kac müsterinin bilgisi var ?
df["Customer ID"].nunique()

# Data' da degisiklikler yapacagım icin eğer geri dönersem diye
df1 = df.copy()

df1["total_price"] = df1["Quantity"] * df1["Price"]

df1.head()

# Bir musterinin toplam ne kadar harcama yaptıgını gormek icin
df1.groupby("Customer ID").agg({"total_price": "sum"}).head()

# 12346 nin iade yaptigi gorulmekte peki Invoice numaraları farkli mi bu iki islemin ?
df1[df1["Customer ID"] == 12346.0]

# Invocie numaraları farklı ... Kac iade olduguna bakmak icin
df1[df1["Invoice"].astype("str").str.get(0) == "C"].shape

# 9288 adet iade oldugunu gördüm.
# İade edilmeyenleri almak icin
df1 = df1[df1["Invoice"].astype("str").str.get(0) != "C"]

# Eksik degerleri bulunan satırlardan kurtulmak icin
df1 = df1.dropna()

# En son yapılan Invoice zamanına bakmak icin
df1["InvoiceDate"].max()

# Bundan sonra Customer ID'leri integer hale getirmek için
df1["Customer ID"] = df1["Customer ID"].astype("int")

##Recency
today_date = dt.datetime(2011, 12, 9)
today_date

rec = today_date - df1.groupby("Customer ID").agg({"InvoiceDate": "max"})
rec.head()

# Days yazısını kaldırmak icin
rec["InvoiceDate"] = rec["InvoiceDate"].apply(lambda x: x.days)
rec["InvoiceDate"].head()

rec.rename(columns={"InvoiceDate": "Recency"}, inplace=True)

rec.head()

##Frequency


# Nunique ile essiz fatura sayısını bulduk
df1.groupby("Customer ID").agg({"Invoice": "nunique"}).head()

df1.groupby("Customer ID").agg({"Invoice": "nunique"}).count()

# Bir gun icerisinde bir kac kere gelindigini de anlayabiliriz buradan


freq = df1.groupby("Customer ID").agg({"InvoiceDate": "nunique"}).rename(columns={"InvoiceDate": "Frequency"})

freq.head()

##Monetary


money = df1.groupby("Customer ID").agg({"total_price": "sum"}).rename(columns={"total_price": "Monetary"})

money.head()

# Boyutlari kontrol etmek icin
print(rec.shape, freq.shape, money.shape)

# Concat
rfm = pd.concat([rec, freq, money], axis=1)
rfm.head()

# RFM Skorlari

rfm["Recency_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["Frequency_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["Monetary_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])
rfm.head()

rfm["RFM"] = rfm["RFM"] = rfm["Recency_Score"].astype(str) + rfm["Frequency_Score"].astype(str) + rfm[
    "Monetary_Score"].astype(str)

rfm.head()

seg_map = {
    r'[1-2][1-2]': "Hibernating",
    r'[1-2][3-4]': "At Risk",
    r'[1-2]5': "Can't Lose",
    r'3[1-2]': "About to Sleep",
    r'33': "Need Attention",
    r'[3-4][4-5]': "Loyal Customers",
    r'41': "Promising",
    r'51': "New Customers",
    r'[4-5][2-3]': "Potential Loyalist", r'5[4-5]': "Champions"}

rfm["Segment"] = rfm["Recency_Score"].astype(str) + rfm["Frequency_Score"].astype(str)
rfm["Segment"] = rfm["Segment"].replace(seg_map, regex=True)
rfm.head()

rfm[["Segment", "Recency", "Frequency", "Monetary"]].groupby("Segment").agg(["min", "max", "mean", "count"])

df2 = pd.DataFrame()

df2["LoyalCustomersID"] = rfm[rfm["Segment"] == "Loyal Customers"].index

df2.head()

df2.to_excel('LoyalCustomersID.xlsx', index=False, header=True)



