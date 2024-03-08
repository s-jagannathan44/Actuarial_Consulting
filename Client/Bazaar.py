import pandas as pd
import glob
import fiscalyear
import duckdb as db
import itertools

year = 0

state_dict = {"Andhra Pradesh": "South", "Arunachal Pradesh": "East", "Assam": "East", "Bihar": "East",
              "Chhattisgarh": "North", "Goa": "West",
              "Gujarat": "west", "Haryana": "North", "Himachal Pradesh": "North", "Jammu and Kashmir": "North",
              "Jharkhand": "East", "Karnataka": "South",
              "Kerala": "South", "Madhya Pradesh": "North", "Maharashtra": "West", "Manipur": "East",
              "Meghalaya": "East", "Mizoram": "East",
              "Nagaland": "East", "Orissa": "East", "Punjab": "North", "Rajasthan": "North", "Sikkim": "East",
              "Tamil Nadu": "South", "TELANGANA": "South",
              "Chattisgarh": "North", "Tripura": "East", "Uttar Pradesh": "North", "UTTARAKHAND": "North",
              "West Bengal": "East",
              "Ladakh": "North", "Andaman & Nicobar Islands": "South", "Chandigarh": "North",
              "Dadra & Nagar Haveli": "West", "Daman & Diu": "West", "Lakshadweep": "South", "Delhi": "North",
              "Pondicherry": "South"}


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
    df["Zone"] = df["registration_state"].apply(lambda x: map_zone(x))
    df.to_csv("base_file.csv")


def map_zone(state):
    try:
        return state_dict[state]
    except KeyError:
        print("Zone mapping error")
        return ""


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
    df["Policy Number"] = df["Policy Number"].apply(lambda x: "PB_" + str(x))
    df.to_csv("claims_file.csv")


def set_financial_year(year_p):
    global count
    try:
        return year_p.to_period('Q-MAR').qyear
    except AttributeError:
        count = count + 1
        print("error occurred in set_financial_year")
        return ""


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


def funct_lt(xy):
    fy = fiscalyear.FiscalYear(int(year) + 3)
    date_diff = xy - fy.start
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
    long_term = db.sql("""select * from master where newplancategory like '%Long Term%' """).df()
    master = db.sql("""select * from master where newplancategory not like '%Long Term%' """).df()
    long_term['policy_end_date'] = long_term['policy_end_date'] + pd.DateOffset(years=2)
    long_term.to_csv("lt.csv")
    fiscalyear.setup_fiscal_calendar(start_month=4)
    for year_ in master["Financial_Year"].unique().tolist():
        year = year_
        df = master[master["Financial_Year"] == year_]
        x = df["policy_start_date"].apply(lambda xz: func(xz))
        y = df["policy_end_date"].apply(lambda xx: funct(xx))
        master.loc[master.Financial_Year == year_, "FY" + str(year_)] = x
        master.loc[master.Financial_Year == year_, "FY" + str(year_ + 1)] = y
        master.loc[master.Financial_Year == year_, "FY" + str(year_) + "_EP"] = (master.loc[master.Financial_Year ==
                                                                                            year_, "FY" + str(year_)]
                                                                                 * master.loc[master.Financial_Year ==
                                                                                              year_, "full_premium"])
        master.loc[master.Financial_Year == year_, "FY" + str(year_ + 1) + "_EP"] = (master.loc[master.Financial_Year ==
                                                                                                year_, "FY" + str(
            year_ + 1)]
                                                                                     * master.loc[
                                                                                         master.Financial_Year ==
                                                                                         year_, "full_premium"])

        print(year_)
    for year__ in long_term["Financial_Year"].unique().tolist():
        year = year__
        df_ = long_term[long_term["Financial_Year"] == year__]
        ax = df_["policy_start_date"].apply(lambda xz: func(xz))
        ay = df_["policy_end_date"].apply(lambda xx: funct_lt(xx))
        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__)] = ax
        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 1)] = 1
        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 2)] = 1
        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 3)] = ay
        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__) + "_EP"] = (
                long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__)]
                * (long_term.loc[long_term.Financial_Year == year__, "full_premium"]) / 3)

        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 1) + "_EP"] = (
                long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 1)]
                * (long_term.loc[long_term.Financial_Year == year__, "full_premium"]) / 3)

        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 2) + "_EP"] = (
                long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 2)]
                * (long_term.loc[long_term.Financial_Year == year__, "full_premium"]) / 3)

        long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 3) + "_EP"] = (
                long_term.loc[long_term.Financial_Year == year__, "FY" + str(year__ + 3)]
                * (long_term.loc[long_term.Financial_Year == year__, "full_premium"]) / 3)

        print(year__)

    exposure = pd.concat([master, long_term], axis=0)
    exposure.to_csv("premium_07_03.csv")


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


def transform_premium_file():
    global norm_policy
    frames = pd.DataFrame()
    years = premium["Financial_Year"].unique().tolist()
    years.append(2025)
    years.append(2026)
    years.append(2027)
    for yearn in years:
        yearly_frame = pd.DataFrame(pd.DataFrame(columns=["PolicyID", "Exposure", "EP"]))
        exp_name = "FY" + str(yearn)
        ep_name = "FY" + str(yearn) + "_EP"
        yearly_frame[["PolicyID", "Exposure", "EP"]] = premium[["PolicyID", exp_name, ep_name]]
        yearly_frame["Accident_Year"] = yearn
        frames = pd.concat([frames, yearly_frame], axis=0)
    nep = db.sql("select * from frames where Exposure is not null and EP is not null").df().sort_values(by="PolicyID")
    # policy.to_csv("modified.csv")
    norm_policy = premium.merge(nep, on="PolicyID")
    norm_policy = norm_policy.loc[:, ~norm_policy.columns.str.startswith('FY20')]
    norm_policy.to_csv("modified_premium.csv")


def find_missing(policy_number):
    if policy_number not in merged:
        return policy_number
    return ''


count = 0
# merge_files()
# merge_claims()
# create_master()
# calculate_exposure()
# premium = pd.read_csv("premium_07_03.csv")
# transform_premium_file()
# premium.rename(columns={"policyno": "Policy_Number"}, inplace=True)

norm_policy = pd.read_csv("modified_premium.csv")
norm_policy.rename(columns={"policyno": "Policy_Number"}, inplace=True)
claims = pd.read_csv("claims_file.csv")
claims.rename(columns={"Policy Number": "Policy_Number"}, inplace=True)
claims.rename(columns={"Claim Reference": "Claim_Reference"}, inplace=True)

claims['Report Date'] = claims['Report Date'].str.replace('-', '')
claims['Claim Closed Date'] = claims['Claim Closed Date'].str.replace('-', '')
claims['Loss Date'] = pd.to_datetime(claims['Loss Date'], format="mixed", dayfirst=True)
claims['Report Date'] = pd.to_datetime(claims['Report Date'], format="%d%m%Y", dayfirst=True)
claims['Claim Closed Date'] = pd.to_datetime(claims['Claim Closed Date'], format="%d%m%Y", dayfirst=True)
claims["Loss_FY"] = claims["Loss Date"].apply(lambda x: set_financial_year(x))
claims["Reported_FY"] = claims["Report Date"].apply(lambda x: set_financial_year(x))
claims["Paid_FY"] = claims["Claim Closed Date"].apply(lambda x: set_financial_year(x))

claims_policy = claims.merge(premium, on=["Policy_Number"], how="inner")
claims_policy.to_csv("Policy_Claim_07_03.csv")
claims["Accident_Year"] = claims["Loss Date"].apply(lambda x: set_financial_year(x))

for col_ in norm_policy.columns:
    if "Unnamed" in col_:
        norm_policy.drop(col_, axis=1, inplace=True)

policy_claims = norm_policy.merge(claims, on=["Policy_Number", "Accident_Year"], how="left")
policy_claims["Claim_Reference"].fillna(0, inplace=True)
policy_claims["Claim count"] = policy_claims["Claim_Reference"].apply(lambda x: 0 if x == 0 else 1)
policy_claims["Total Claim"] = policy_claims["Paid"] = policy_claims["OS"]
policy_claims["Long term"] = policy_claims["newplancategory"].apply(lambda x: "LT" if "Long Term" in x else "ST")
policy_claims["Policy Count"] = policy_claims["Long term"].apply(lambda x: 0.25 if x == "LT" else 0.5)
df_ = policy_claims[policy_claims["Long term"] == "ST"]
df_["Adjusted full premium"] = df_["full_premium"] / 2.0
lt_frame = policy_claims[policy_claims["Long term"] == "LT"]
lt_frame["Adjusted full premium"] = lt_frame["full_premium"] / 4.0
policy_claims = pd.concat([df_, lt_frame], axis=0)

policy_claims.to_csv("merged_claims_07_03.csv")
print(count)


def extract_missing():
    global claims_policy, claims, merged
    claims_policy = pd.read_csv("Policy_Claim_07_03.csv")
    claims = pd.read_csv("claims_file.csv")
    merged = claims_policy["Policy_Number"].tolist()
    claims["Missing_Claims"] = claims["Policy Number"].apply(lambda x: find_missing(x))
    claims.to_csv("missing.csv")

# df["Cause Of Loss"].fillna("-",inplace=True)
# filtered_df = df[df['Cause Of Loss'].str.contains('Death')]
# injury_df = df[~ df['Cause Of Loss'].str.contains('Death')]
# pv =pd.pivot_table(filtered_df, values="Accident_Year", columns=["Policy Number", "Cause Of Loss"],
#                          aggfunc="count").T.to_csv("dcount.csv")
# gic = pd.pivot_table(filtered_df, values="Total_Claim", columns=["Policy Number", "Cause Of Loss"],
#                          aggfunc="sum").T.to_csv("dgic.csv")
