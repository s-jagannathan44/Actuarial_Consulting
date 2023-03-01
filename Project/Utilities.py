import pandas as pd


def extract_policies():
    df = pd.read_csv("Output\\2W Policy Data JAN 232W_Policy.csv", encoding='windows-1252')

    PolicyNos = ["P0018100004/4102/106939", "P0018100006/4102/107427", "P0018200014/4102/104137",
                 "P0019100004/4112/100310", "P0019200014/4113/102481", "P0019200014/4113/103884",
                 "P0019200014/4113/105999", "P0019200014/4113/106096", "P0019200014/4113/106773",
                 "P0019400007/4113/102284", "P0019400007/4113/104110", "P0019400023/4113/103014",
                 "P0020400020/4113/106471"]
    Grouped = pd.DataFrame(columns=df.columns)
    for PolicyNo in PolicyNos:
        rows = df[df["Policy No"] == PolicyNo]
        Grouped = Grouped.append(rows)

    Grouped.to_csv("Output\\Row.csv")


def process_paid_claims():
    # df = pd.read_csv('Output\\TW Paid ITD Dec 2022 v1.csv')
    # df["UniqueKey"] = df["Policy No"] + df["RSD New"]
    df = pd.read_csv("Output\\Data\\Project\\PaidClaims.csv")
    df = df[df["Paid FY"] != "2022-23"]
    col_list = ["Policy No", "Type", "NOL Flag", "Date of Loss", "Paid FY", "RSD New", "UniqueKey"]
    df = df.groupby(col_list).sum()
    df.to_csv("Output\\Grouped.csv")


def process_outstanding_claims():
    df = pd.read_csv("Output\\Data\\Project\\Claims_Outstanding.csv")
    df = df[df["OS AS ON"] == "01-03-2022"]
    Grouped = pd.DataFrame(columns=df.columns)
    df["UniqueKey"] = df["Policy No"] + df["RSD New"]
    ClaimNos = df["Claim No"].unique()
    for ClaimNo in ClaimNos:
        Claims = df[df["Claim No"] == ClaimNo]
        Claim = Claims.iloc[len(Claims) - 1]
        Grouped = Grouped.append(Claim)

    Grouped.to_csv("Output\\Outstanding.csv")


def sum_columns(df):
    GEP_List = ["GEP 1213", "GEP 1314", "GEP 1415", "GEP 1516", "GEP 1617", "GEP 1718", "GEP 1819", "GEP 1920",
                "GEP 2021", "GEP 2122"]
    NEP_List = ["NEP 1213", "NEP 1314", "NEP 1415", "NEP 1516", "NEP 1617", "NEP 1718", "NEP 1819", "NEP 1920",
                "NEP 2021", "NEP 2122"]
    Exposure_List = ["EXPO 1213", "EXPO 1314", "EXPO 1415", "EXPO 1516", "EXPO 1617", "EXPO 1718", "EXPO 1819",
                     "EXPO 1920", "EXPO 2021", "EXPO 2122"]
    col_to_drop = GEP_List + NEP_List + Exposure_List + ["GEP 2223", "NEP 2223", "EXPO 2223"]

    # df = pd.read_csv("Output\\VerticalAddition.csv")
    df['NEP'] = df[NEP_List].sum(axis=1)
    df["Exposure"] = df[Exposure_List].sum(axis=1)
    df["GEP"] = df[GEP_List].sum(axis=1)
    df.drop(columns=col_to_drop, axis=1, inplace=True)

    for col in df.columns:
        if "Unnamed" in col:
            df.drop(col, axis=1, inplace=True)
    return df
    # df.to_csv("Output\\Sum.csv")


def group_policies(df):
    col_list = ["Policy No", "LT_ANNUAL Flag", "RSD New", "UniqueKey", "CC_desc", "Body Type", "Vehicle Make",
                "V AGE BAND", "Zone", "UniqueKey"]
    # df = pd.read_csv("Output\\Make.csv")
    df = df.groupby(col_list).sum()
    return df
    # df.to_csv("Output\\VerticalAddition.csv")


def combine_make():
    df = pd.read_csv("Output\\Data\\Project\\Project.csv")
    df["UniqueKey"] = df["Policy No"] + df["RSD New"]
    Makes = ["HERO", "BAJAJ", "HONDA", "TVS", "YAMAHA", "ROYALENFIELD", "SUZUKI"]
    list_makes = df["Vehicle Make"].unique()
    OtherMakes = []

    for Make in list_makes:
        if Makes.count(Make) == 0:
            OtherMakes.append(Make)

    for Make in Makes:
        df.loc[df['Vehicle Make'].str.startswith(Make, na=False), 'Vehicle Make'] = Make

    for Make in OtherMakes:
        df.loc[df['Vehicle Make'].str.startswith(Make, na=False), 'Vehicle Make'] = "OTHER"
    return df
    #  df.to_csv("Output\\Make.csv")


def process_policies():
    df = combine_make()
    df = group_policies(df)
    df = sum_columns(df)
    df.to_csv("Output\\Final.csv")


process_policies()
