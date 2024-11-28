# import DoubleLift
import pandas as pd
from sklearn.model_selection import train_test_split
import duckdb as db


def group_bucket(x):
    if 0 < x <= 10:
        return "Bucket 1"
    elif 10 < x <= 20:
        return "Bucket 2"
    elif 20 < x <= 30:
        return "Bucket 3"
    elif 30 < x <= 40:
        return "Bucket 4"
    elif 40 < x <= 50:
        return "Bucket 5"
    if 50 < x <= 60:
        return "Bucket 6"
    elif 60 < x <= 70:
        return "Bucket 7"
    elif 70 < x <= 80:
        return "Bucket 8"
    elif 80 < x <= 90:
        return "Bucket 9"
    else:
        return "Bucket 10"


frame = pd.DataFrame(columns=["Bucket", "Start", "End"])
tiles = 100
start = 0
end = 100 / tiles
for i in range(tiles):
    frame.loc[i] = [round(i + 1, 0), start, end]
    start = frame.loc[i]["End"]
    end = (start + 100 / tiles)
print(frame.head(tiles))


def group_dynamic_bucket(x):
    for r in frame.iterrows():
        Start = r[1]["Start"]
        End = r[1]["End"]
        if Start < x <= End:
            return "Bucket " + str(int(r[1]["Bucket"]))
        elif x > 100:
            return "Bucket " + str(int(r[1]["Bucket"]))


def Simple_Quantile_Plot():
    df_ = pd.read_csv("Star_Charts.csv")
    df__, df = train_test_split(df_, test_size=0.1, random_state=0)
    df = df.sort_values(by='Pred_Cost', axis=0, ascending=True)
    df['cumpct'] = df['LIVES_EXPOSED'].cumsum() / df['LIVES_EXPOSED'].sum() * 100
    df["Bucket"] = df["cumpct"].apply(lambda x: group_bucket(x))
    # df.to_csv("tile.csv")
    q3 = """select Bucket, sum(LIVES_EXPOSED) as Exposure, sum(Pred_Cost) as Predicted, sum(PAID_AMT) as Actual,                       
            from df            
            group by  Bucket           
     """
    output = db.execute(q3).df()
    output.to_csv("tile.csv")


def Scatter_Plot():
    df_ = pd.read_csv("Star_Charts.csv")
    df__, df = train_test_split(df_, test_size=0.1, random_state=0)
    df = df.sort_values(by='Pred_Cost', axis=0, ascending=True)
    df['cumpct'] = df['LIVES_EXPOSED'].cumsum() / df['LIVES_EXPOSED'].sum() * 100
    df["Bucket"] = df["cumpct"].apply(lambda x: group_dynamic_bucket(x))
    df.to_csv("tile.csv")
    q3 = """select Bucket, sum(LIVES_EXPOSED) as Exposure, sum(Pred_Cost) as Predicted, sum(PAID_AMT) as Actual,                       
            from df            
            group by  Bucket           
     """
    output = db.execute(q3).df()
    output.to_csv("tile.csv")


# Simple_Quantile_Plot()
Scatter_Plot()
# DoubleLift.DoubleLift(df[" Pred_Cost "], df[" Pred_Cost "], df[" PAID_AMT "],
#                       weight=df[" LIVES_EXPOSED "], model_key=df["Key"])

# df.sort_values(by="Pred_Cost", inplace=True)
# # df["runtot_weight"] = df["LIVES_EXPOSED"].cumsum()
# df["p_tile"] = pd.cut(df["LIVES_EXPOSED"], 10, labels=False)
# df.to_csv("tile.csv")
# df_ChartAgg = df.groupby("p_tile").agg(model1_agg=("Pred_Cost", 'mean'),
#                                        actual_agg=("PAID_AMT", 'mean'))
# # df_ChartAgg["model1_agg"] = df_ChartAgg.model1_num_agg / df_ChartAgg.y_denom_agg
# # df_ChartAgg["actual_agg"] = df_ChartAgg.actual_num_agg / df_ChartAgg.y_denom_agg
# #
# df_ChartAgg = df_ChartAgg.filter(items=["actual_agg", "model1_agg", "p_tile"])
# pass
