import pandas as pd
import joblib
from sklearn.linear_model import TweedieRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def build_model():
    column_trans = ColumnTransformer(
        [
            ('OHE', OneHotEncoder(),
             ("make_name_new model_name_new transmission_type fuel_type_new previous_supplier_name_new  cc_range "
              "vehicle_details_segment_new supplier_name_new policy_type registration_rto_code_new seating_capacity_new "
              "revised_plan_category_new ncb age_range idv_slot_new  revised_is_cng_fitted_new  is_health_pb_customer "
              "is_claims_made_in_previous_policy is_two_wheeler_pb_customer is_travel_pb_customer    "
              "lead_day_slot_new expiry_type_new is_ep is_coc is_rsa is_key_rep is_inpc is_bi_fuel_kit_liability "
              "is_term_life_pb_customer is_tp_pd_liability")
             .split()),
        ],
    )
    tweedie_glm = Pipeline(
        [
            ("transform", column_trans),
            ("regressor", TweedieRegressor(alpha=1.0, power=1.9)),
        ]
    )
    tweedie_glm.fit(
        df_model, df["Loss_Cost"], regressor__sample_weight=df["LIVES_EXPOSED"]
    )
    joblib.dump(tweedie_glm, "Tweedie.sav")
    return tweedie_glm  # , column_trans


df = pd.read_csv("Output\\4WheelerFile.csv")
df = df[df["LIVES_EXPOSED"] > 0]
df["Loss_Cost"] = df["PAID_AMT"] / df["LIVES_EXPOSED"]
df["Loss_Cost"].fillna(0, inplace=True)
df_model = df[("make_name_new model_name_new transmission_type fuel_type_new previous_supplier_name_new  cc_range "
               "vehicle_details_segment_new supplier_name_new policy_type registration_rto_code_new seating_capacity_new "
               "revised_plan_category_new ncb age_range idv_slot_new  revised_is_cng_fitted_new  is_health_pb_customer "
               "is_claims_made_in_previous_policy is_two_wheeler_pb_customer is_travel_pb_customer    "
               "lead_day_slot_new expiry_type_new is_ep is_coc is_rsa is_key_rep is_inpc is_bi_fuel_kit_liability "
               "is_term_life_pb_customer is_tp_pd_liability").split()]
model = build_model()
y_pred = model.predict(df)
df["Pred"] = y_pred
df["Pred_Cost"] = df["Pred"] * df["LIVES_EXPOSED"]
df.to_csv("Output\\Tweedie_4wheelerOutput.csv")
