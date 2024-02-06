import pandas as pd
import glob
import fiscalyear
import duckdb as db

year = 0

state_dict ={"Andhra Pradesh": "South","Arunachal Pradesh":"East","Assam":"East","Bihar":"East","Chhattisgarh":"North","Goa":"West",
"Gujarat":"west","Haryana":"North","Himachal Pradesh":"North","Jammu and Kashmir":"North","Jharkhand":"East","Karnataka":"South",
"Kerala":"South","Madhya Pradesh":"North","Maharashtra":"West","Manipur":"East","Meghalaya":"East","Mizoram":"East",
"Nagaland":"East","Orissa":"East","Punjab":"North","Rajasthan":"North","Sikkim":"East","Tamil Nadu":"South","TELANGANA":"South",
"Chattisgarh":"North","Tripura":"East","Uttar Pradesh":"North","UTTARAKHAND":"North","West Bengal":"East",
"Ladakh":"North","Andaman & Nicobar Islands":"South","Chandigarh":"North",
"Dadra & Nagar Haveli":"West","Daman & Diu":"West","Lakshadweep":"South","Delhi":"North","Pondicherry":"South"}


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
    except:
        print(state)

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
    global count
    try:
        return year_p.to_period('Q-MAR').qyear
    except AttributeError:
        count = count + 1
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
    exposure.to_csv("premium.csv")


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
    long_term = db.sql("""select * from exposure where newplancategory like '%Long Term%' """).df()
    short_term = db.sql("""select * from exposure where newplancategory not like '%Long Term%' """).df()

    for year_ in short_term["Financial_Year"].unique().tolist():
        exposure["FY" + str(year_) + "_EP"] = exposure["FY" + str(year_)] * exposure["full_premium"]
    for year_ in long_term["Financial_Year"].unique().tolist():
        exposure["FY" + str(year_) + "_EP"] = exposure["FY" + str(year_)] * (exposure["full_premium"] / 3.0)

    exposure.to_csv("premium.csv")


def find_missing(policy_number):
    if policy_number not in merged:
        return policy_number
    return ''


merge_files()
merge_claims()
count = 0
create_master()
calculate_exposure()

premium = pd.read_csv("premium.csv")
claims = pd.read_csv("claims_file.csv")
claims['Report Date'] = claims['Report Date'].str.replace('-', '')
claims['Claim Closed Date'] = claims['Claim Closed Date'].str.replace('-', '')

# datetime.strptime("01121017", "%d%m%Y")

claims['Loss Date'] = pd.to_datetime(claims['Loss Date'], format="mixed", dayfirst=True)
claims['Report Date'] = pd.to_datetime(claims['Report Date'], format="%d%m%Y", dayfirst=True)
claims['Claim Closed Date'] = pd.to_datetime(claims['Claim Closed Date'], format="%d%m%Y", dayfirst=True)

for col_ in premium.columns:
    if "Unnamed" in col_:
        premium.drop(col_, axis=1, inplace=True)

premium.rename(columns={"policyno": "Policy Number"}, inplace=True)
claims["Policy Number"] = claims["Policy Number"].apply(lambda x: "PB_" + str(x))
claims_policy = claims.merge(premium, on=["Policy Number"], how="inner")
merged = claims_policy["Policy Number"].tolist()
claims["Missing_Claims"] = claims["Policy Number"].apply(lambda x: find_missing(x))
claims_policy["Loss_FY"] = claims_policy["Loss Date"].apply(lambda x: set_financial_year(x))
claims_policy["Reported_FY"] = claims_policy["Report Date"].apply(lambda x: set_financial_year(x))
claims_policy["Paid_FY"] = claims_policy["Claim Closed Date"].apply(lambda x: set_financial_year(x))
claims_policy.to_csv("Policy_Claim.csv")
claims.to_csv("missing.csv")
