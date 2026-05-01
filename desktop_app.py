import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib

# 1. Define the custom function used in your pipeline BEFORE loading the model
def drop_columns(df):
    """Replicates the column-dropping logic from your Jupyter Notebook."""
    # return df.drop(columns=['building_id'], errors='ignore')
    return df

# 2. Load the trained Machine Learning Model
try:
    model = joblib.load("rfc_pipeline.pkl")
except Exception as e:
    model = None
    print(f"Failed to load model. Ensure 'rfc_pipeline.pkl' is in the same folder. Error: {e}")

# 3. Create the main application window
root = tk.Tk()
root.title("Earthquake Damage Predictor")
root.geometry("450x600")
root.configure(padx=20, pady=20)

# 4. Define the Prediction Function
def make_prediction():
    if model is None:
        messagebox.showerror("Error", "Model not loaded. Cannot make predictions.")
        return

    try:
        # Gather inputs from the GUI
        input_data = {
            "geo_level_1_id": int(geo_var.get()),
            "geo_level_2_id": 487, # Default filler
            "geo_level_3_id": 12198, # Default filler
            "count_floors_pre_eq": int(floors_var.get()),
            "age": int(age_var.get()),
            "area_percentage": 6,
            "height_percentage": 5,
            "land_surface_condition": "t",
            "foundation_type": foundation_var.get().split(" ")[0], # Extract the letter code
            "roof_type": roof_var.get().split(" ")[0],
            "ground_floor_type": ground_floor_var.get().split(" ")[0],
            "other_floor_type": "q",
            "position": "t",
            "plan_configuration": "d",
            "has_superstructure_adobe_mud": 0,
            "has_superstructure_mud_mortar_stone": 1,
            "has_superstructure_stone_flag": 0,
            "has_superstructure_cement_mortar_stone": 0,
            "has_superstructure_mud_mortar_brick": 0,
            "has_superstructure_cement_mortar_brick": 0,
            "has_superstructure_timber": 0,
            "has_superstructure_bamboo": 0,
            "has_superstructure_rc_non_engineered": 0,
            "has_superstructure_rc_engineered": 0,
            "has_superstructure_other": 0,
            "legal_ownership_status": "v",
            "count_families": 1,
            "has_secondary_use": 0,
            "has_secondary_use_agriculture": 0,
            "has_secondary_use_hotel": 0,
            "has_secondary_use_rental": 0,
            "has_secondary_use_institution": 0,
            "has_secondary_use_school": 0,
            "has_secondary_use_industry": 0,
            "has_secondary_use_health_post": 0,
            "has_secondary_use_gov_office": 0,
            "has_secondary_use_use_police": 0,
            "has_secondary_use_other": 0
        }

        # Convert to Pandas DataFrame and Predict
        input_df = pd.DataFrame([input_data])
        prediction = model.predict(input_df)[0]

        # Update the UI with the result
        if prediction == 1:
            result_label.config(text="Grade 1: Low Damage\nMinor structural wear expected.", fg="green")
        elif prediction == 2:
            result_label.config(text="Grade 2: Medium Damage\nModerate structural damage expected.", fg="orange")
        else:
            result_label.config(text="Grade 3: Complete Destruction\nHigh risk of collapse.", fg="red")

    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all text boxes contain valid numbers.")
    except Exception as e:
        messagebox.showerror("Prediction Error", str(e))

# 5. Build the User Interface (UI)
tk.Label(root, text="🏠 Earthquake Damage Predictor", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

# Variables to store user input
geo_var = tk.StringVar(value="6")
age_var = tk.StringVar(value="30")
floors_var = tk.StringVar(value="2")
foundation_var = tk.StringVar(value="r (Mud/Stone)")
roof_var = tk.StringVar(value="n (Light)")
ground_floor_var = tk.StringVar(value="f (Mud)")

# Input Fields
tk.Label(root, text="Geo Level 1 ID:", font=("Helvetica", 10, "bold")).pack(anchor="w")
tk.Entry(root, textvariable=geo_var).pack(fill="x", pady=(0, 10))

tk.Label(root, text="Age (Years):", font=("Helvetica", 10, "bold")).pack(anchor="w")
tk.Entry(root, textvariable=age_var).pack(fill="x", pady=(0, 10))

tk.Label(root, text="Floors Before EQ:", font=("Helvetica", 10, "bold")).pack(anchor="w")
tk.Entry(root, textvariable=floors_var).pack(fill="x", pady=(0, 10))

tk.Label(root, text="Foundation Type:", font=("Helvetica", 10, "bold")).pack(anchor="w")
ttk.Combobox(root, textvariable=foundation_var, values=["r (Mud/Stone)", "w (Bamboo/Timber)", "i (RC)", "u (Other)", "h (Other)"], state="readonly").pack(fill="x", pady=(0, 10))

tk.Label(root, text="Roof Type:", font=("Helvetica", 10, "bold")).pack(anchor="w")
ttk.Combobox(root, textvariable=roof_var, values=["n (Light)", "q (Heavy)", "x (RC)"], state="readonly").pack(fill="x", pady=(0, 10))

tk.Label(root, text="Ground Floor Type:", font=("Helvetica", 10, "bold")).pack(anchor="w")
ttk.Combobox(root, textvariable=ground_floor_var, values=["f (Mud)", "x (Brick/Stone)", "v (RC)", "z (Timber)", "m (Other)"], state="readonly").pack(fill="x", pady=(0, 20))

# Predict Button
tk.Button(root, text="Predict Damage Grade", command=make_prediction, bg="#0078D7", fg="white", font=("Helvetica", 12, "bold"), pady=5).pack(fill="x")

# Result Display
result_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), pady=20)
result_label.pack()

# 6. Run the Application
if __name__ == "__main__":
    root.mainloop()