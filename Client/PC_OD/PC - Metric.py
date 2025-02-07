# import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import duckdb as db


def ConvertCategoricalToNumeric():
    df['fuel_type'] = df['fuel_type'].str.replace('Petrol', "0")
    df['fuel_type'] = df['fuel_type'].str.replace('Diesel', "1")
    df['fuel_type'] = df['fuel_type'].str.replace('CNG', "2")
    df['fuel_type'] = df['fuel_type'].str.replace('LPG', "3")
    df['fuel_type'] = df['fuel_type'].str.replace('Electric', "4")
    df['lead_day_slot'] = df['lead_day_slot'].str.replace('daytime', "0")
    df['lead_day_slot'] = df['lead_day_slot'].str.replace('early', "1")
    df['lead_day_slot'] = df['lead_day_slot'].str.replace('evening', "2")
    df['lead_day_slot'] = df['lead_day_slot'].str.replace('late_night', "3")
    df['lead_day_slot'] = df['lead_day_slot'].str.replace('night', "4")
    df['expiry_type'] = df['expiry_type'].str.replace('Active', "0")
    df['expiry_type'] = df['expiry_type'].str.replace('BrandNew', "1")
    df['expiry_type'] = df['expiry_type'].str.replace('BreakIn', "2")
    df['expiry_type'] = df['expiry_type'].str.replace('Others', "3")
    df['type_of_cng_kit'] = df['type_of_cng_kit'].str.replace('No', "0")
    df['type_of_cng_kit'] = df['type_of_cng_kit'].str.replace('ExternallyFitted', "1")
    df['type_of_cng_kit'] = df['type_of_cng_kit'].str.replace('CompanyFitted', "2")
    df['policy_type'] = df['policy_type'].str.replace('New', "0")
    df['policy_type'] = df['policy_type'].str.replace('Renewal', "1")
    df['policy_type'] = df['policy_type'].str.replace('Rollover', "2")
    df['previous_insurer_type'] = df['previous_insurer_type'].str.replace('psu', "0")
    df['previous_insurer_type'] = df['previous_insurer_type'].str.replace('pvt', "1")
    df['fuel_type'] = pd.to_numeric(df['fuel_type'], downcast='integer', errors='coerce')
    df['lead_day_slot'] = pd.to_numeric(df['lead_day_slot'], downcast='integer', errors='coerce')
    df['expiry_type'] = pd.to_numeric(df['expiry_type'], downcast='integer', errors='coerce')
    df['type_of_cng_kit'] = pd.to_numeric(df['type_of_cng_kit'], downcast='integer', errors='coerce')
    df['policy_type'] = pd.to_numeric(df['policy_type'], downcast='integer', errors='coerce')
    df['previous_insurer_type'] = pd.to_numeric(df['previous_insurer_type'], downcast='integer', errors='coerce')
    df['owner_sr'] = pd.to_numeric(df['owner_sr'], downcast='integer', errors='coerce')


def DumpNullToCSV():
    global df
    df = pd.read_csv("CSV\\Ultimate_fixed.csv")
    df[df["is_paid_y"].isna()]["Policy_Number"].value_counts().to_csv("Output\\is_paid.csv")
    df[df["t_booking_y"].isna()]["Policy_Number"].value_counts().to_csv("Output\\t_booking_y.csv")
    df[df["t_parent_y"].isna()]["Policy_Number"].value_counts().to_csv("Output\\t_parent_y.csv")
    df[df["previous_supplier_name"].isna()]["Policy_Number"].value_counts().to_csv("Output\\previous_supplier_name.csv")
    df[df["previous_ncb_y"].isna()]["Policy_Number"].value_counts().to_csv("Output\\previous_ncb_y.csv")
    df[df["ncb_y"].isna()]["Policy_Number"].value_counts().to_csv("Output\\ncb_y.csv")


def persons_correlation():
    # set figure size
    plt.figure(figsize=(10, 7))
    # Generate a mask to only show the bottom triangle
    mask = np.triu(np.ones_like(df.corr(method='pearson'), dtype=bool))
    # generate heatmap
    sns.heatmap(df.corr(method='pearson'), annot=True, mask=mask, vmin=-1, vmax=1)
    plt.title('Correlation Coefficient Of Predictors')
    plt.show()


# compute the vif for all given features
def compute_vif(considered_features):
    X = df[considered_features]
    # the calculation of variance inflation requires a constant
    X['intercept'] = 1

    # create dataframe to store vif values
    vif = pd.DataFrame()
    vif["Variable"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif = vif[vif['Variable'] != 'intercept']
    return vif


df = pd.read_csv("CSV\\FixedMultiplier\\Combined_final_file.csv", usecols=(
    "vehicle_age  transmission_type  fuel_type   cubic_capacity opted_kms policy_type seating_capacity "
    "is_cng_fitted type_of_cng_kit  previous_ncb  NCB  is_health_pb_customer  previous_insurer_type  previous_policy_type "
    "is_claims_made_in_previous_policy is_two_wheeler_pb_customer  is_travel_pb_customer is_term_life_pb_customer lead_day_slot "
    "expiry_type is_ep is_coc sum_insured  is_rsa  is_key_rep   is_inpc is_bi_fuel_kit_liability is_tp_pd_liability  t_booking  t_parent  owner_sr"
).split())
ConvertCategoricalToNumeric()
df = df.dropna(subset=['vehicle_age', 'NCB', 'previous_ncb', 'transmission_type', 'type_of_cng_kit', "owner_sr", "previous_policy_type"])
# df.corr(method='pearson').to_csv("Output\\corr.csv")
persons_correlation()

# ----------------------------   VIF  ------------------------------------

# considered_feature = ['vehicle_age', 'expiry_type', "policy_type", 'ncb_y', 'previous_ncb_y', 'is_inpc', 'fuel_type',
#                       'transmission_type', 'is_ep', 'is_coc', 'is_rsa', 'is_key_rep', 'seating_capacity']
#
# # compute vif
# compute_vif(considered_feature).sort_values('VIF', ascending=False)
# ----------------------------   VIF   ------------------------------------


# df = pd.read_csv("CSV\\Ultimate_fixed.csv", usecols=["type_of_cng_kit", "opted_kms"])
#
# crosstab = pd.crosstab(df["type_of_cng_kit"], df["opted_kms"])
# val = stats.chi2_contingency(crosstab)
# pass
