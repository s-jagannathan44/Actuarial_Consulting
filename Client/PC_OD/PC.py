import pandas as pd
import glob
import fiscalyear
import duckdb as db
import math

count = 0
year = 0


def merge_files():
    path = "Booking/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        df = pd.concat([df, frame], axis=0)
    df.to_csv("CSV\\base_file.csv")


def merge_claims():
    path = "Claims/*.csv"
    df = pd.DataFrame()
    files = glob.glob(path)
    for file_name in files:
        frame = pd.read_csv(file_name)
        new_frame = pd.DataFrame(
            columns=["Claim_Reference", "Policy_Number", "Insurer_Name", "product_type", "Loss Date",
                     "Report Date", "Claim Closed Date", "kind_of_loss", "cause_of_loss",
                     "registration_no", "total_paid", "total_os", "status", "file_date", "incurred"])
        print(file_name)
        if "claim_number" in frame.columns:
            new_frame["Claim_Reference"] = frame["claim_number"]
        if "policy_num" in frame.columns:
            new_frame["Policy_Number"] = frame["policy_num"]
        if "insurer_name" in frame.columns:
            new_frame["Insurer_Name"] = frame["insurer_name"]
        if "producttype" in frame.columns:
            new_frame["product_type"] = frame["producttype"]
        elif "ProductType" in frame.columns:
            new_frame["product_type"] = frame["ProductType"]
        else:
            new_frame["product_type"] = frame["product_type"]
        if "loss_date" in frame.columns:
            new_frame["Loss Date"] = frame["loss_date"]
        elif "Loss_Date" in frame.columns:
            new_frame["Loss Date"] = frame["loss_date"]
        if "intimation_date" in frame.columns:
            new_frame["Report Date"] = frame["intimation_date"]
        if "claim_close_date" in frame.columns:
            new_frame["Claim Closed Date"] = frame["claim_close_date"]
        if "kind_of_loss" in frame.columns:
            new_frame["kind_of_loss"] = frame["kind_of_loss"]
        if "cause_of_loss" in frame.columns:
            new_frame["cause_of_loss"] = frame["cause_of_loss"]
        if "registration_no" in frame.columns:
            new_frame["registration_no"] = frame["registration_no"]
        if "total_paid" in frame.columns:
            new_frame["total_paid"] = frame["total_paid"]
        if "total_os" in frame.columns:
            new_frame["total_os"] = frame["total_os"]
        if "status" in frame.columns:
            new_frame["status"] = frame["status"]
        if "file_date" in frame.columns:
            new_frame["file_date"] = frame["file_date"]
        if "incurred" in frame.columns:
            new_frame["incurred"] = frame["incurred"]
        elif "Incurred" in frame.columns:
            new_frame["incurred"] = frame["Incurred"]
        else:
            new_frame["incurred"] = frame["total_incurred"]

        df = pd.concat([df, new_frame], axis=0)
    df.to_csv("CSV\\claims_file.csv")


def prefix_pb(pno):
    policy_no = str(pno)
    if policy_no.startswith('PB'):
        return policy_no
    else:
        return "PB_" + policy_no


def set_financial_year(year_p):
    global count
    try:
        return year_p.to_period('Q-MAR').qyear
    except AttributeError:
        count = count + 1
        print("error occurred in set_financial_year")
        return ""


def transform_claim():
    claims = pd.read_csv("CSV\\claims_file.csv")
    claims['Loss Date'] = pd.to_datetime(claims['Loss Date'], format="mixed", dayfirst=True)
    claims['Report Date'] = pd.to_datetime(claims['Report Date'], format="mixed", dayfirst=True)
    claims['Claim Closed Date'] = pd.to_datetime(claims['Claim Closed Date'], format="mixed", dayfirst=True)
    claims["Accident_Year"] = claims["Loss Date"].apply(lambda x: set_financial_year(x))
    claims["Reported_FY"] = claims["Report Date"].apply(lambda x: set_financial_year(x))
    claims["Paid_FY"] = claims["Claim Closed Date"].apply(lambda x: set_financial_year(x))
    claims["Policy_Number"] = claims["Policy_Number"].apply(lambda x: prefix_pb(x))
    return claims


def create_master():
    col_list = (
        "vehicle_age  registered_state_name  registered_city_name  zone  registration_rto_code  make_name  model_name  variant_name  transmission_type  fuel_type  "
        "cubic_capacity  vehicle_details_segment  sum_insured  is_bi_fuel_kit  t_booking  t_parent  t_booking_slot  t_parent_slots  is_pg  is_paid  is_zd  is_ep  "
        "is_lpb  is_coc  is_pa  is_rsa  is_daily_ac  is_key_rep  is_ncb_pr  is_windshield  is_inpc  is_electrical_accessories  is_non_electrical_accessories  "
        "is_bi_fuel_kit  is_bi_fuel_kit_liability  is_pa_for_unnamed_passenger  is_compulsory_pa_cover_for_owner_driver  is_legal_liability_to_paid_driver  i"
        "s_tp_pd_liability  is_voluntary_discount  previous_policy_type  previous_ncb  is_claims_made_in_previous_policy  t_booking  is_zd  lead_day_slot  "
        "is_health_pb_customer  is_travel_pb_customer  is_two_wheeler_pb_customer  is_term_life_pb_customer  owner_sr  is_investment_pb_customer  final_premium"
        "  uw_start_date  uw_end_date  pb_date  ncb  lead_id  policy_no  policy_type  policy_start_date  policy_end_date  opted_kms  previous_policy_expiry_date  "
        "manufacturing_date  registration_date  is_cng_fitted  type_of_cng_kit  seating_capacity  previous_supplier_name  cc_range  new_plan_category  expiry_type  "
        "age_range  idv_slot  booking_month  uw_month  uw_year previous_supplier_name supplier_name previous_insurer_type")

    base = pd.read_csv("CSV\\base_file.csv", usecols=col_list.split())
    base['policy_start_date'] = pd.to_datetime(base['policy_start_date'], format="mixed", dayfirst=True)
    base = base.sort_values(by='policy_start_date')
    base["Financial_Year"] = base["policy_start_date"].apply(lambda x: set_financial_year(x))
    base.to_csv("CSV\\master.csv")


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


def calculate_exposure():
    global year
    master = pd.read_csv("CSV\\master.csv")
    master['policy_start_date'] = pd.to_datetime(master['policy_start_date'], format="mixed", dayfirst=True)
    master['policy_end_date'] = pd.to_datetime(master['policy_end_date'], format="mixed", dayfirst=True)
    fiscalyear.setup_fiscal_calendar(start_month=4)
    fy_l = master["Financial_Year"].unique().tolist()

    for year_ in fy_l:
        year = year_
        if math.isnan(year):
            break
        df = master[master["Financial_Year"] == year_]
        x = df["policy_start_date"].apply(lambda xz: func(xz))
        y = df["policy_end_date"].apply(lambda xx: funct(xx))
        master.loc[master.Financial_Year == year_, "FY" + str(year_)] = x
        master.loc[master.Financial_Year == year_, "FY" + str(year_ + 1)] = y

        master.loc[master.Financial_Year == year_, "FY" + str(year_) + "_EP"] = (master.loc[master.Financial_Year ==
                                                                                            year_, "FY" + str(year_)]
                                                                                 * master.loc[master.Financial_Year ==
                                                                                              year_, "final_premium"])
        master.loc[master.Financial_Year == year_, "FY" + str(year_ + 1) + "_EP"] = (master.loc[master.Financial_Year ==
                                                                                                year_, "FY" + str(
            year_ + 1)]
                                                                                     * master.loc[
                                                                                         master.Financial_Year ==
                                                                                         year_, "final_premium"])

        print(year_)
    for col_ in master.columns:
        if "Unnamed" in col_:
            master.drop(col_, axis=1, inplace=True)

    master.to_csv("CSV\\premium.csv")


def transform_premium_file():
    global norm_policy
    frames = pd.DataFrame()
    years = premium["Financial_Year"].unique().tolist()
    for yearn in years:
        if math.isnan(yearn):
            break
        yearly_frame = pd.DataFrame(pd.DataFrame(columns=["index", "Exposure", "EP"]))
        exp_name = "FY" + str(yearn)
        ep_name = "FY" + str(yearn) + "_EP"
        yearly_frame[["index", "Exposure", "EP"]] = premium[["index", exp_name, ep_name]]
        yearly_frame["Accident_Year"] = yearn
        frames = pd.concat([frames, yearly_frame], axis=0)
        print(yearn)
    nep = premium.merge(frames, on="index")
    norm_policy = db.sql("select * from nep where Exposure is not null and EP is not null").df()
    for col_ in norm_policy.columns:
        if "Unnamed" in col_:
            norm_policy.drop(col_, axis=1, inplace=True)
    norm_policy.to_csv("CSV\\modified_premium.csv")


# merge_files()
# merge_claims()
# claims = transform_claim()
# claims.to_csv("CSV\\claims_file_v2.csv")
claims = pd.read_csv("CSV\\claims_file_v2.csv")
create_master()
calculate_exposure()
premium = pd.read_csv("CSV\\premium.csv")
premium.rename(columns={"Unnamed: 0": "index"}, inplace=True)
transform_premium_file()

norm_policy = pd.read_csv("CSV\\modified_premium.csv")
for col__ in norm_policy.columns:
    if "Unnamed" in col__:
        norm_policy.drop(col__, axis=1, inplace=True)
norm_policy.rename(columns={"policy_no": "Policy_Number"}, inplace=True)
policy = norm_policy.merge(claims, on=["Policy_Number", "Accident_Year"], how="left")
policy["Claim_Reference"].fillna(0, inplace=True)
policy["Claim count"] = policy["Claim_Reference"].apply(lambda x: 0 if x == 0 else 1)
claim_count = db.sql(
    """ select Policy_number, Accident_Year, count(Claim_Reference) as count  from policy group by Policy_number, Accident_Year """).df()

q2 = """select policy.Policy_number, policy.Accident_Year,  EP/count  as Normalized_Earned_Premium,
         Exposure/count as Normalized_LIVES_EXPOSED,
        from policy join claim_count
        on policy.Policy_number =claim_count.Policy_number and policy.Accident_Year = claim_count.Accident_Year"""
nep = db.execute(q2).df()
norm_policy = policy.merge(nep, on=["Policy_Number", "Accident_Year"])
norm_policy = norm_policy.drop_duplicates(subset=['Policy_Number', 'Accident_Year', "Claim_Reference"])

for col__ in norm_policy.columns:
    if "Unnamed" in col__:
        norm_policy.drop(col__, axis=1, inplace=True)

norm_policy.to_csv("CSV\\policy_claims_analysis.csv")

# df = pd.read_csv("CSV\\policy_claims_analysis.csv")
#
# df = df[df["supplier_name"].str.contains("United")]
# df.to_csv("Output\\United.csv")

# policy = pd.read_csv("CSV\\policy_claims_analysis.csv")
# # df = pd.read_csv("Output\\OrientalPremium.csv")
# claim_count = db.sql(
#     """ select Policy_number, Accident_Year, count(Claim_Reference) as count  from policy group by Policy_number, Accident_Year """).df()
#
# q2 = """select policy.Policy_number, policy.Accident_Year,  EP/count  as Normalized_Earned_Premium,
#          Exposure/count as Normalized_LIVES_EXPOSED,
#         from policy join claim_count
#         on policy.Policy_number =claim_count.Policy_number and policy.Accident_Year = claim_count.Accident_Year"""
# nep = db.execute(q2).df()
# # nep.to_csv("Output\\count.csv")
# norm_policy = policy.merge(nep, on=["Policy_Number", "Accident_Year"])
# norm_policy = norm_policy.drop_duplicates(subset=['Policy_Number', 'Accident_Year', "Claim_Reference"])
# norm_policy.to_csv("Output\\nep.csv")

# claim_count = db.sql(
#     """ select Policy_number, Accident_Year, sum(Exposure), count(Claim_Reference) as count  from df group by Policy_number, Accident_Year """).df()
# claim_count.to_csv("Output\\cc.csv")


# Code to read all column headers dump them to a file  we can Identify files where headers are spelt differently
# path = "Claims/*.csv"
# df = pd.DataFrame()
# files = glob.glob(path)
# for file_name in files:
#     frame = pd.read_csv(file_name)
#     frame.dtypes.to_csv("Columns\\" + file_name[7:-4] + ".csv")
#
# path = "Columns/*.csv"
# df = pd.DataFrame()
# files = glob.glob(path)
# for file_name in files:
#     client_name = file_name[8:-4]
#     frame = pd.read_csv(file_name)
#     frame["Policy_Client_Name"] = client_name
#
#     df = pd.concat([df, frame], axis=0)
#     df.to_csv("cols.csv")


# path = "Claims/*.csv"
# df = pd.DataFrame()
# files = glob.glob(path)
# for file_name in files:
#     frame = pd.read_csv(file_name)
#     print(file_name)
#     df[file_name[7:-4]] = pd.Series(frame.columns)
#
# df.to_csv("Output\\claims.csv")

#
# claims = pd.read_csv("Claims\\Final United Claims_JV.csv")
# base = pd.read_csv("Booking\\United_Bkgs_2021_04_2024_03.csv")
# base['Key'] = base["policy_no"].str[-6:]
# claims['Key'] = claims["policy_num"].str[-6:]
# claim_policy = pd.merge(claims, base[['Key', 'policy_no']], on=['Key'], how='left')
# # claim_policy = claims.merge(base, on="Key")
# claim_policy.to_csv("Output\\United.csv")
