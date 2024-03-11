import pandas as pd
import glob
import fiscalyear
import duckdb as db

year = 0

state_dict = {"Andhra Pradesh": "South", "Arunachal Pradesh": "East", "Assam": "East", "Bihar": "East",
              "Chhattisgarh": "North", "Goa": "West",
              "Gujarat": "west", "Haryana": "North", "Himachal Pradesh": "North", "Jammu and Kashmir": "North",
              "Jharkhand": "East", "Karnataka": "South", "Jammu & Kashmir": "North", "NCR": "North",
              'Odisha': "East", "Telangana": "South", "Pondicherry": "South",
              "Kerala": "South", "Madhya Pradesh": "North", "Maharashtra": "West", "Manipur": "East",
              "Meghalaya": "East", "Mizoram": "East", "Uttarakhand": "North",
              "Nagaland": "East", "Orissa": "East", "Punjab": "North", "Rajasthan": "North", "Sikkim": "East",
              "Tamil Nadu": "South", "TELANGANA": "South",
              "Chattisgarh": "North", "Tripura": "East", "Uttar Pradesh": "North", "UTTARAKHAND": "North",
              "West Bengal": "East",
              "Ladakh": "North", "Andaman & Nicobar Islands": "South", "Chandigarh": "North",
              "Dadra & Nagar Haveli": "West", "Daman & Diu": "West", "Lakshadweep": "South", "Delhi": "North",
              "Andaman and Nicobar Islands": "South", "Dadra and Nagar Haveli": "West", "Daman and Diu": "West",
              }


def merge_files():
    path = "Bazaar/TW/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        client_name = file_name[7:-12]
        frame = pd.read_csv(file_name)
        frame["Policy_Client_Name"] = client_name
        df = pd.concat([df, frame], axis=0)
    df["Zone"] = df["registrationstate"].apply(lambda x: map_zone(x))
    df.rename(columns={"policyno": "Policy_Number"}, inplace=True)
    df["Policy_Number"] = df["Policy_Number"].apply(lambda x: "PB_" + str(x))
    df = df.drop_duplicates(subset=["Policy_Number"])
    for col_ in df.columns:
        if "Unnamed" in col_:
            df.drop(col_, axis=1, inplace=True)
    keys = range(1, 1 + len(df))
    df.insert(0, 'index', keys)
    df.to_csv("Bazaar\\Output\\base_file.csv")


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
    path = "Bazaar/TW/Claims/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        client_name = file_name[14:-8]
        frame = pd.read_csv(file_name)
        frame["Client_Name"] = client_name
        df = pd.concat([df, frame], axis=0)
    df.dropna(subset=['Claim Reference'], inplace=True)
    df["Policy Number"] = df["Policy Number"].apply(lambda x: "PB_" + str(x))
    df.to_csv("Bazaar\\Output\\claims_file.csv")


def set_financial_year(year_p):
    global count
    try:
        return year_p.to_period('Q-MAR').qyear
    except AttributeError:
        count = count + 1
        print("error occurred in set_financial_year")
        return ""


def create_master():
    base = pd.read_csv("Bazaar\\Output\\base_file.csv")
    base.rename(columns={"policy_startdate": "policy_start_date"}, inplace=True)
    base.rename(columns={"policy_enddate": "policy_end_date"}, inplace=True)
    base = transform_data(base)
    base = base.sort_values(by='policy_start_date')
    base["Financial_Year"] = base["policy_start_date"].apply(lambda x: set_financial_year(x))
    for col_ in base.columns:
        if "Unnamed" in col_:
            base.drop(col_, axis=1, inplace=True)

    base.to_csv("Bazaar\\Output\\master.csv")


def transform_data(exposure):
    exposure['policy_start_date'] = pd.to_datetime(exposure['policy_start_date'], format="mixed", dayfirst=True)
    exposure["irda_tp"] = exposure['irda_tp'].apply(lambda x: convert_premium(x))
    exposure["full_premium"] = exposure["irda_tp"]
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
    if x in [482, 538]:
        return "Below 75cc"
    elif x in [714, 752]:
        return "75 to 150cc"
    elif x in [1193, 1366]:
        return "150 to 350cc"
    elif x in [2323, 2804]:
        return "Above 350cc"


def group_body_type(x):
    if "Activa" in x or "DIO" in x or "Destini" in x or "Xoom" in x or "PLEASURE" in x \
            or "CHETAK" in x or "jupiter" in x or "scooty" in x or "zest" in x or "ntorq" in x \
            or "aerox" in x or "rayzr" in x or "moto gp" in x or "fascino" in x or "burgman" in x \
            or "avenis" in x or "access" in x or "vespa" in x:
        return "Scooter"
    else:
        return "Bike"


def calculate_exposure():
    global year
    master = pd.read_csv("Bazaar\\Output\\master.csv")
    master['policy_start_date'] = pd.to_datetime(master['policy_start_date'], format="mixed", dayfirst=True)
    master['policy_end_date'] = pd.to_datetime(master['policy_end_date'], format="mixed", dayfirst=True)
    long_term = db.sql("""select * from master where irda_tp >3000 """).df()
    master = db.sql("""select * from master where irda_tp <3000 """).df()
    long_term['policy_end_date'] = long_term['policy_end_date'] + pd.DateOffset(years=2)

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
                                                                                                year_, "FY" + str(year_ + 1)]
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
    for col_ in exposure.columns:
        if "Unnamed" in col_:
            exposure.drop(col_, axis=1, inplace=True)

    exposure.to_csv("Bazaar\\Output\\premium.csv")


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
    for yearn in years:
        yearly_frame = pd.DataFrame(pd.DataFrame(columns=["index", "Exposure", "EP"]))
        exp_name = "FY" + str(yearn)
        ep_name = "FY" + str(yearn) + "_EP"
        yearly_frame[["index", "Exposure", "EP"]] = premium[["index", exp_name, ep_name]]
        yearly_frame["Accident_Year"] = yearn
        frames = pd.concat([frames, yearly_frame], axis=0)
    nep = db.sql("select * from frames where Exposure is not null and EP is not null").df()
    # policy.to_csv("modified.csv")
    norm_policy = premium.merge(nep, on="index")
    norm_policy = norm_policy.loc[:, ~norm_policy.columns.str.startswith('FY20')]
    for col_ in norm_policy.columns:
        if "Unnamed" in col_:
            norm_policy.drop(col_, axis=1, inplace=True)
    norm_policy.to_csv("Bazaar\\Output\\modified_premium.csv")


# def find_missing(policy_number):
#     if policy_number not in merged:
#         return policy_number
#     return ''


def transform_claim():
    global claims
    claims = pd.read_csv("Bazaar\\Output\\claims_file.csv")
    claims.rename(columns={"Policy Number": "Policy_Number"}, inplace=True)
    claims.rename(columns={"Claim Reference": "Claim_Reference"}, inplace=True)
    claims['Report Date'] = claims['Report Date'].str.replace('-', '')
    claims['Claim Closure Date'] = claims['Claim Closure Date'].str.replace('-', '')
    claims['Loss Date'] = pd.to_datetime(claims['Loss Date'], format="mixed", dayfirst=True)
    claims['Report Date'] = pd.to_datetime(claims['Report Date'], format="%d%m%Y", dayfirst=True)
    claims['Claim Closure Date'] = pd.to_datetime(claims['Claim Closure Date'], format="%d%m%Y", dayfirst=True)
    claims["Loss_FY"] = claims["Loss Date"].apply(lambda x: set_financial_year(x))
    claims["Reported_FY"] = claims["Report Date"].apply(lambda x: set_financial_year(x))
    claims["Paid_FY"] = claims["Claim Closure Date"].apply(lambda x: set_financial_year(x))
    return claims


count = 0
# merge_files()
# merge_claims()
# create_master()
# calculate_exposure()
premium = pd.read_csv("Bazaar\\Output\\premium.csv")
# transform_premium_file()

norm_policy = pd.read_csv("Bazaar\\Output\\modified_premium.csv")
claims = transform_claim()
claims_policy = claims.merge(premium, on=["Policy_Number"], how="inner")
claims_policy.to_csv("Bazaar\\Output\\Policy_Claim.csv")
claims["Accident_Year"] = claims["Loss Date"].apply(lambda x: set_financial_year(x))

for col__ in norm_policy.columns:
    if "Unnamed" in col__:
        norm_policy.drop(col__, axis=1, inplace=True)

policy_claims = norm_policy.merge(claims, on=["Policy_Number", "Accident_Year"], how="left")
policy_claims["Claim_Reference"].fillna(0, inplace=True)
policy_claims["Claim count"] = policy_claims["Claim_Reference"].apply(lambda x: 0 if x == 0 else 1)
policy_claims["Total Claim"] = policy_claims["Final Paid"] = policy_claims["Final OS"]
policy_claims["Long term"] = policy_claims["irda_tp"].apply(lambda x: "LT" if x > 3000 else "ST")
policy_claims["Policy Count"] = policy_claims["Long term"].apply(lambda x: 0.25 if x == "LT" else 0.5)
st_frame = policy_claims[policy_claims["Long term"] == "ST"]
st_frame["Adjusted full premium"] = st_frame["full_premium"] / 2.0
lt_frame = policy_claims[policy_claims["Long term"] == "LT"]
lt_frame["Adjusted full premium"] = lt_frame["full_premium"] / 4.0
policy_claims = pd.concat([st_frame, lt_frame], axis=0)

policy_claims["ccnew"] = policy_claims["full_premium"].apply(lambda x: group_cubic_capacity(x))
policy_claims["body_type"] = policy_claims["modelname"].apply(lambda x: group_body_type(x))

for col__ in policy_claims.columns:
    if "Unnamed" in col__:
        policy_claims.drop(col__, axis=1, inplace=True)

policy_claims.to_csv("Bazaar\\Output\\merged_claims.csv")
print(count)

# def extract_missing():
#     global claims_policy, claims, merged
#     claims_policy = pd.read_csv("Policy_Claim_07_03.csv")
#     claims = pd.read_csv("claims_file.csv")
#     merged = claims_policy["Policy_Number"].tolist()
#     claims["Missing_Claims"] = claims["Policy Number"].apply(lambda x: find_missing(x))
#     claims.to_csv("missing.csv")
