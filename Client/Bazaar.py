import pandas as pd
import glob
import fiscalyear

year = 0


def merge_files():
    path = "Bazaar/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        client_name = file_name[7:-12]
        frame = pd.read_csv(file_name)
        frame["Policy_Client_Name"] = client_name
        df = pd.concat([df, frame], axis=0)
    df["PolicyID"] = df["PolicyID"].apply(lambda x: prefix_pb(str(x)))
    df.to_csv("base_file.csv")


def prefix_pb(policy_no):
    if policy_no.startswith('PB'):
        return policy_no
    else:
        return "PB_" + policy_no


def merge_claims():
    path = "Bazaar/Claims/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        client_name = file_name[14:-8]
        frame = pd.read_csv(file_name)
        frame["Client_Name"] = client_name
        df = pd.concat([df, frame], axis=0)
    df.dropna(subset=['Claim Reference'], inplace=True)
    df.to_csv("claims_file.csv")


def set_financial_year(year_p):
    return year_p.to_period('Q-MAR').qyear


def create_master():
    base = pd.read_csv("base_file.csv")
    base = transform_data(base)
    base = base.sort_values(by='policy_start_date')
    base["Financial_Year"] = base["policy_start_date"].apply(lambda x: set_financial_year(x))
    base.to_csv("master.csv")


def transform_data(exposure):
    exposure['policy_start_date'] = pd.to_datetime(exposure['policy_start_date'], format="mixed", dayfirst=True)
    exposure["tp_premium"] = exposure['tp_premium'].apply(lambda x: convert_premium(x))
    exposure["tp_addons"] = exposure['tp_addons'].apply(lambda x: convert_premium(x))
    exposure["full_premium"] = exposure["tp_premium"] + exposure["tp_addons"]
    exposure["cubiccapacity_New"] = exposure["cubiccapacity"].apply(lambda x: group_cubic_capacity(x))
    return exposure


def func(xy):
    fy = fiscalyear.FiscalYear(int(year))
    date_diff = fy.end - xy
    exposure = date_diff / (fy.end - fy.start)
    return exposure


def funct(xy):
    fy = fiscalyear.FiscalYear(int(year) + 1)
    date_diff = xy - fy.start
    exposure = date_diff / (fy.end - fy.start)
    return exposure


def group_cubic_capacity(x):
    if x < 1000:
        return "Below 1000cc"
    elif 1000 < x < 1500:
        return "1000 to 1500cc"
    elif x > 1500:
        return "Above 1500cc"


def calculate_exposure():
    global year
    master = pd.read_csv("master.csv")
    master['policy_start_date'] = pd.to_datetime(master['policy_start_date'], format="mixed", dayfirst=True)
    master['policy_end_date'] = pd.to_datetime(master['policy_end_date'], format="mixed", dayfirst=True)

    fiscalyear.setup_fiscal_calendar(start_month=4)
    for year_ in master["Financial_Year"].unique().tolist():
        year = year_
        df = master[master["Financial_Year"] == year_]
        x = df["policy_start_date"].apply(lambda xz: func(xz))
        y = df["policy_end_date"].apply(lambda xx: funct(xx))
        master.loc[master.Financial_Year == year_, "FY" + str(year_)] = x
        master.loc[master.Financial_Year == year_, "FY" + str(year_ + 1)] = y
        print(year_)
    master.to_csv("exposure.csv")


def convert_premium(prem):
    global count
    if isinstance(prem, str):
        prem = prem[:-3]
        try:
            # noinspection PyTypeChecker
            digits = ''.join(filter(str.isdigit, prem))
            return float(digits)
        except ValueError:
            count = count + 1
            print("faced an error with {}".format(str(count) + prem))
            return 0.0
    else:
        return float(prem)


def calculate_earned_premium():
    exposure = pd.read_csv("exposure.csv")
    for col in exposure.columns:
        if "Unnamed" in col:
            exposure.drop(col, axis=1, inplace=True)
    for year_ in exposure["Financial_Year"].unique().tolist():
        exposure["FY" + str(year_) + "_EP"] = exposure["FY" + str(year_)] * exposure["full_premium"]
    exposure.to_csv("premium.csv")


def find_missing(policy_number):
    if policy_number not in merged:
        return policy_number
    return ''


# merge_files()
# merge_claims()
count = 0
# create_master()
# master = pd.read_csv("master.csv")
# df2 = pd.pivot_table(master, values="full_premium", columns="Client_Name", aggfunc="sum")
# df2 = df2.transpose()
# print(df2)

# calculate_exposure()
# calculate_earned_premium()


premium = pd.read_csv("premium.csv")
claims = pd.read_csv("claims_file.csv")
for col_ in premium.columns:
    if "Unnamed" in col_:
        premium.drop(col_, axis=1, inplace=True)

premium.rename(columns={"policyno": "Policy Number"}, inplace=True)
claims["Policy Number"] = claims["Policy Number"].apply(lambda x: "PB_" + str(x))
claims_policy = claims.merge(premium, on=["Policy Number"], how="inner")
merged = claims_policy["Policy Number"].tolist()
claims["Missing_Claims"] = claims["Policy Number"].apply(lambda x: find_missing(x))
claims_policy.to_csv("Policy_Claim.csv")
claims.to_csv("missing.csv")
