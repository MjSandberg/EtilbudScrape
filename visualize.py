# %%
import pandas as pd 
import matplotlib.pyplot as plt
from os.path import exists

def IQR(df):
    # Interquartile Range
    q1, q3 = df["Pris"].quantile([0.25, 0.75])
    iqr = q3-q1
    ind = (df["Pris"] < (q1 - 1.5 * iqr)) |(df["Pris"] > (q3 + 1.5 * iqr))
    df2 = df[~ind]
    
    return df2

def reader(file):
    df = pd.read_csv(file)
    df["Dato"] = pd.to_datetime(df["Dato"], dayfirst=True, format="%d.%m.%Y")
    return df

def PriceTime(item, df):
    df = df.sort_values(by="Dato")
    plt.figure(figsize=(20,10))
    plt.xticks(rotation=45)
    plt.title(f"pris af {item} over tid")
    for enhed in df["Enhed"].unique():
        df3 = df[df["Enhed"]==enhed]
        if len(df3)==1:    
            plt.plot(df3["Dato"].dt.strftime('%d.%m.%Y'), df3["Pris"], "o", label=f"{enhed}")
        else:
            plt.plot(df3["Dato"].dt.strftime('%d.%m.%Y'), df3["Pris"], label=f"{enhed}")
        
    plt.legend()
    return plt.show()
    
def main():
    mode = input("Almen (1), Sammenlign (2), Tilbud (3): ")
    services = ["coop", "rema", "tilbud_data"]
    item = input("What item: ")
    file_coop = service[0] + "/" + item + ".txt"
    file_rema = service[1] + "/" + item + ".txt"
    file_tilbud = service[2] + "/" + item + ".txt"
    
    if exists(file_coop): df_coop = reader(file_coop)
    if exists(file_rema): df_rema = reader(file_rema)
    if exists(file_tilbud): df_tilbud = reader(file_tilbud)
    # Subplots med alle forskellige
    
    if mode=="1":
        item = input("What item: ")
        for service in services:
            file = service + "/" + item + ".txt"
            if exists(file):
                df = reader(file)
                PriceTime(item+ f" fra {service}", df)
                
    elif mode=="2":
        item = input("What item: ")
        
        plt.figure(figsize=(20,10))
        plt.xticks(rotation=45)
        plt.title(f"pris af {item} over tid")
        first = True
        for service in services:
            file = service + "/" + item + ".txt"
            if exists(file):
                df = reader(file)
                df = df.sort_values(by="Dato")
                if first:
                    first = False
                    print(df["Enhed"].unique())
                    enhed = input("Select Unit: ")
                
                df3 = df[df["Enhed"]==enhed]
                plt.plot(df3["Dato"].dt.strftime('%d.%m.%Y'), df3["Pris"], label=f"{service} {enhed}")

        plt.legend()
        plt.show()
                
    elif mode=="3":
        item = input("What item: ")
        service = "tilbud_data"
        file = service + "/" + item + ".txt"
        df = reader(file)
        df = IQR(df)
        PriceTime(item, df)
        
            
        
    
if __name__ == '__main__':
    main()
    
    
# %%

# # item = input("What item: ")
# item = "jordbær"
# file = "tilbud_data/" + item + ".txt"
# df = pd.read_csv(file)
# df["Dato"] = pd.to_datetime(df["Dato"], dayfirst=True, format="%d.%m.%Y")
# #df["Dato"] = df["Dato"].dt.strftime('%d.%m.%Y')

# # Interquartile Range
# q1, q3 = df["Pris"].quantile([0.25, 0.75])
# iqr = q3-q1
# ind = (df["Pris"] < (q1 - 1.5 * iqr)) |(df["Pris"] > (q3 + 1.5 * iqr))
# df2 = df[~ind]
# df2 = df2.sort_values(by="Dato")

# # %%
# plt.figure()
# plt.xticks(rotation=45)
# plt.title(f"pris af {item} over tid")
# for enhed in df2["Enhed"].unique():
#     print(enhed)
#     df3 = df2[df2["Enhed"]==enhed]
#     if len(df3)==1:    
#         plt.plot(df3["Dato"].dt.strftime('%d.%m.%Y'), df3["Pris"], "o", label=f"{enhed}")
#     else:
#         plt.plot(df3["Dato"].dt.strftime('%d.%m.%Y'), df3["Pris"], label=f"{enhed}")
    
    
# plt.legend()
    
    