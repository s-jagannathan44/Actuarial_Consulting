import pandas as pd
from datetime import datetime, timedelta
import duckdb as db

mdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# Constants for months referenced later
February = 2
month = ""


def is_leap(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def month_len(year, month_):
    return mdays[month_] + (month_ == February and is_leap(year))


def get_months():
    df = pd.read_csv("Bazaar\\Month_list.csv")
    return df["Months"].unique().tolist()


def func(xy):
    test_date = datetime.strptime(month, "%m-%d-%Y")
    days_in_month = month_len(test_date.year, test_date.month)
    days_in_year = 365

    if is_leap(test_date.year):
        days_in_year = 366

    end_date = (test_date + timedelta(days_in_month - 1))
    exposure = ((end_date - xy).days + 1) / days_in_year
    return exposure


def funct(xy):
    test_date = datetime.strptime(month, "%m-%d-%Y")
    days_in_year = 365

    if is_leap(test_date.year):
        days_in_year = 366

    exposure = ((xy - test_date).days + 1) / days_in_year
    return exposure


def funcs():
    test_date = datetime.strptime(month, "%m-%d-%Y")
    days_in_month = month_len(test_date.year, test_date.month)
    days_in_year = 365

    if is_leap(test_date.year):
        days_in_year = 366

    exposure = days_in_month / days_in_year
    return exposure


def calculate_exposure():
    master = pd.read_csv("Bazaar\\Bajaj_Booking_Dump 4th Jun'21 to 23th Sep'24.csv")
    # master = pd.read_csv("Bazaar\\Trial.csv")
    master['uw_startdate'] = pd.to_datetime(master['uw_startdate'], format="mixed", dayfirst=True)
    master["uw_enddate"] = pd.to_datetime(master['uw_enddate'], format="mixed", dayfirst=True)
    master["tp_addon"] = 0

    # master = master[
    #     master['uw_enddate'] > '2023-01-01']  # 1st step to exclude all policies with end date before Jan 23
    month_list = get_months()

    for month_ in month_list:
        global month
        month = month_
        print(month)
        test_date = datetime.strptime(month, "%m-%d-%Y")
        days_in_month = month_len(test_date.year, test_date.month)

        # 2nd  step to find policies with start date in current month
        df1 = master[
            (master["uw_startdate"] >= month) & (master["uw_startdate"] <= (test_date + timedelta(days_in_month - 1)))]

        # 3rd step is to find policies with end date in current month
        df2 = master[
            (master["uw_enddate"] >= month) & (master["uw_enddate"] <= (test_date + timedelta(days_in_month - 1)))]

        # 4th step is to find policies which pass through the month
        df3 = master[
            (master["uw_startdate"] < month) & (master["uw_enddate"] > (test_date + timedelta(days_in_month - 1)))]

        start_exposure = df1["uw_startdate"].apply(lambda xz: func(xz))
        end_exposure = df2["uw_enddate"].apply(lambda xx: funct(xx))
        passthrough_exposure = df3["uw_startdate"].apply(lambda xz: funcs())
        exposure_month = str(test_date.month) + "_" + str(test_date.year)
        count = 0
        for exposure in start_exposure:
            index_ = start_exposure.index[count]
            master.at[index_, exposure_month] = exposure
            master.at[index_, exposure_month + "OD_EP"] = master.at[index_, exposure_month] * master.at[index_, "od_ao"]
            master.at[index_, exposure_month + "TP_EP"] = master.at[index_, exposure_month] * (
                    master.at[index_, "tp_rate"] + master.at[index_, "tp_addon"])

            count = count + 1

        count = 0
        for exposure in end_exposure:
            index_ = end_exposure.index[count]
            master.at[index_, exposure_month] = exposure
            master.at[index_, exposure_month + "OD_EP"] = master.at[index_, exposure_month] * master.at[index_, "od_ao"]
            master.at[index_, exposure_month + "TP_EP"] = master.at[index_, exposure_month] * (
                    master.at[index_, "tp_rate"] + master.at[index_, "tp_addon"])
            count = count + 1

        count = 0
        for exposure in passthrough_exposure:
            index_ = passthrough_exposure.index[count]
            master.at[index_, exposure_month] = exposure
            master.at[index_, exposure_month + "OD_EP"] = master.at[index_, exposure_month] * master.at[index_, "od_ao"]
            master.at[index_, exposure_month + "TP_EP"] = master.at[index_, exposure_month] * (
                    master.at[index_, "tp_rate"] + master.at[index_, "tp_addon"])
            count = count + 1

    master.to_csv("Bazaar\\Output\\Bajaj_PC_v2.csv")


def prefix_pb(policy_no):
    if policy_no.startswith('PB'):
        return policy_no
    else:
        return "PB_" + policy_no


def calculate_earned_loss_cost():
    master = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_policy_claims_loss_cost.csv")
    month_list = []
    for col in master.columns:
        if '_202' in col:
            month_list.append(col)

    for month_ in month_list:
        master[month_ + "OD_LC"] = master[month_] * master["LossCost"]
        master[month_ + "TP_LC"] = master[month_] * master["TPLossCost"]

    master.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_policy_claims_elc.csv")


# MERGING POLICY  INTO CLAIMS TWO WHEElER
# norm_policy = pd.read_csv("Bazaar\\Output\\Bajaj_TW_v1.csv")
# df3 = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_TW_Incurred_Claims.csv")
# norm_policy.rename(columns={"policyno": "Policy_Number"}, inplace=True)
# norm_policy = norm_policy[
#     ["Policy_Number", "cor_flag", "uw_month", "booking_date"]]
#
# policy_claims = df3.merge(norm_policy, on=["Policy_Number"], how="left")
# policy_claims.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_TW_claims_final_v5.csv")

# MERGING POLICY  INTO CLAIMS PRIVATE CAR
# norm_policy = pd.read_csv("Bazaar\\Output\\Bajaj_PC_v1.csv")
# df3 = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_Incurred_Claims_update.csv")
# norm_policy.rename(columns={"policyno": "Policy_Number"}, inplace=True)
# df3["Policy_Number"] = df3["Policy_Number"].apply(lambda x: prefix_pb(str(x)))
# norm_policy = norm_policy[
#     ["Policy_Number", "cor_spectrum", "uw_month", "bookingdate", "uw_year"]]
#
# policy_claims = df3.merge(norm_policy, on=["Policy_Number"], how="left")
#
# policy_claims.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_claims_final_v6.csv")


def merge_tw_claims_policy():
    norm_policy = pd.read_csv("Bazaar\\Output\\Bajaj_TW_v1.csv")
    df4 = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_TW_Incurred_Claims.csv")
    norm_policy.rename(columns={"policyno": "Policy_Number"}, inplace=True)
    df4.rename(columns={"Policy Number": "Policy_Number"}, inplace=True)
    df4.rename(columns={"Kind of Loss": "Kind_of_Loss"}, inplace=True)
    q3 = """select sum(Incurred) as Incurred, sum(Claim_Count) as Claim_Count,
            Claim_Reference, Policy_Number, Kind_of_Loss,Loss_Month,Intimation_Month,
            PaidClaimAmount, Outstanding_Amount, File
            from df4
            group by Claim_Reference, Policy_Number, Kind_of_Loss,Loss_Month,Intimation_Month,
            PaidClaimAmount, Outstanding_Amount, File
     """
    claims = db.execute(q3).df()
    claims.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_TW_grouped_claims.csv")
    policy_claims = norm_policy.merge(claims, on=["Policy_Number"], how="left")
    policy_claims["Claim_Reference"].fillna(0, inplace=True)
    policy_claims.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_TW_policy_claims_merge_v2.csv")


def merge_claims_policy():
    norm_policy = pd.read_csv("Bazaar\\Output\\Bajaj_PC_v2.csv")
    df4 = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_Incurred_Claims.csv")
    norm_policy.rename(columns={"policyno": "Policy_Number"}, inplace=True)
    df4.rename(columns={"Policy Number": "Policy_Number"}, inplace=True)
    df4.rename(columns={"Kind of Loss": "Kind_of_Loss"}, inplace=True)
    df4["Policy_Number"] = df4["Policy_Number"].apply(lambda x: prefix_pb(str(x)))
    q3 = """select sum(Incurred) as Incurred, sum(Claim_Count) as Claim_Count,
            Claim_Reference, Policy_Number, Kind_of_Loss,Loss_Month,Intimation_Month,
            PaidClaimAmount, Outstanding_Amount, File
            from df4
            group by Claim_Reference, Policy_Number, Kind_of_Loss,Loss_Month,Intimation_Month,
            PaidClaimAmount, Outstanding_Amount, File
     """
    claims = db.execute(q3).df()
    claims.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_grouped_claims.csv")
    policy_claims = norm_policy.merge(claims, on=["Policy_Number"], how="left")
    policy_claims["Claim_Reference"].fillna(0, inplace=True)
    policy_claims.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_policy_claims_merge_v3.csv")


def merge_loss_cost():
    df = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_policy_claims_merge_v3.csv")
    df = df.drop_duplicates(subset=["Policy_Number"])
    for col in df.columns:
        if 'OD_EP' in col:
            del df[col]
        if 'TP_EP' in col:
            del df[col]
    od_lc = pd.read_csv(
        "C:\\Data\\PB\\Incurred_Sep_2024\\Files\\Bajaj_Full\\CSV\\PC\\Loss Cost Bajaj_Booking_Dump 4th Jun'21 to 23th Sep'24.csv")
    tp_lc = pd.read_csv("C:\\Data\\PB\\Incurred_Sep_2024\\Files\\Bajaj_Full\\CSV\\PC\\Bajaj_TP LossCost.csv")
    od_df = df.merge(od_lc, on=["leadid"], how="left")
    tp_df = od_df.merge(tp_lc, on=["leadid"], how="left")
    tp_df.to_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_policy_claims_loss_cost.csv")


# calculate_exposure()
# merge_claims_policy()
# merge_loss_cost()
# calculate_earned_loss_cost()
# merge_tw_claims_policy()

# df = pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_claims_final_v6.csv")
# df1 = df[df["uw_month"] == "2021_11"]
# df2 = df[df["uw_month"] == "2023_01"]
# # df1.to_csv("2021_11.csv")
# df2.to_csv("2023_01.csv")

# EXTRACTING 5000  SAMPLE CLAIMS
# df_pc =  pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\merged_claims_new_PC.csv")
# df_tw = pd.read_csv("Bazaar\\merged_claims_file_TW.csv")
# df_pc = df_pc[df_pc["PaidClaimAmount"] > 0]
# df_tw = df_tw[df_tw["PaidClaimAmount"] > 0]

# df1 = df_pc[~ df_pc["Kind of Loss"].isin(["TP", "PA"])]
# df_pc["PaidClaimAmount"].sample(n=5000).to_csv("SampleODPCAmounts.csv")
# df2 = df_tw[~ df_tw["Kind_of_Loss"].isin(["TP", "PA"])]
# df2["PaidClaimAmount"].sample(n=5000).to_csv("SampleTWODAmounts.csv")


# EXTRACTING 5000  SAMPLE CLAIM COUNTS
# df_pc =  pd.read_csv("Bazaar\\Output\\Bajaj_PC_claims_final.csv")
# df_tw = pd.read_csv("Bazaar\\Output\\Bajaj_TW_claims_final.csv")
#
# df_pc["Claim_Count"].sample(n=5000).to_csv("SamplePCCounts.csv")
# df_tw["Claim_Count"].sample(n=5000).to_csv("SampleTWCounts.csv")


# EXTRACTING MONTHS WITH lARGE DIFFERENCE BETWEEN OUR INCURRED AND THEIR BENCHMARK
# df =  pd.read_csv("Bazaar\\Output\\FinalRun_03_10\\Bajaj_PC_claims_final_v5.csv")
# df["uw_month"].fillna("_", inplace=True)
# df1 = df[ df["uw_month"].str.contains("2023_06")]
# df2 = df[ df["uw_month"].str.contains("2024_01")]
# df1.to_csv("2023_06.csv")
# df2.to_csv("2024_01.csv")
