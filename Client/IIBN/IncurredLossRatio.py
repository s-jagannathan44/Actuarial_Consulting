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
    master = pd.read_csv("Bazaar\\Combined_Booking_Dump.csv")
    # master = pd.read_csv("Bazaar\\Trial.csv")
    master['uw_startdate'] = pd.to_datetime(master['uw_startdate'], format="mixed", dayfirst=True)
    master["uw_enddate"] = pd.to_datetime(master['uw_enddate'], format="mixed", dayfirst=True)

    master = master[
        master['uw_enddate'] > '2023-01-01']  # 1st step to exclude all policies with end date before Jan 23
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

    master.to_csv("Bazaar\\Output\\ILR_v4.csv")


def prefix_pb(policy_no):
    if policy_no.startswith('PB'):
        return policy_no
    else:
        return "PB_" + policy_no


# calculate_exposure()
norm_policy = pd.read_csv("Bazaar\\Output\\ILR_v4.csv")
df3 = pd.read_csv("Bazaar\\Output\\Combined_Incurred_Claims_v4.csv")

df3["Policy_Number"] = df3["Policy_Number"].apply(lambda x: prefix_pb(str(x)))

q3 = """select sum(Incurred) as Incurred, sum(Claim_Count) as Claim_Count,
            Claim_Reference, Policy_Number, Kind_of_Loss,Loss_Month,Intimation_Month
            from df3 
            group by Claim_Reference, Policy_Number, Kind_of_Loss,Loss_Month,Intimation_Month
     """

claims = db.execute(q3).df()
claims.to_csv("Bazaar\\Output\\grouped_claims.csv")
policy_claims = norm_policy.merge(claims, on=["Policy_Number"], how="left")
policy_claims["Claim_Reference"].fillna(0, inplace=True)
claim_count = db.sql(
    """ select Policy_Number, count(Claim_Reference) as count  from policy_claims group by Policy_Number """).df()
norm_policy = policy_claims.merge(claim_count, on="Policy_Number")


norm_policy.to_csv("Bazaar\\Output\\combined_claims_final.csv")

