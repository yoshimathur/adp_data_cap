import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import glob
from PIL import Image
import os

st.set_page_config(page_title="ADP Final Insights Dashboard", layout="wide")
st.title("📊 ADP Final Insights Dashboard")

# 1. Dropdown for CSV selection
csv_files = {
    "Phase 1 Cleaned Data": "data/phase1_cleaned_data.csv",
    "Cost Analysis": "data/cost_analysis.csv",
    "Benefit Scorecard": "data/benefit_scorecard.csv",
    "Sentiment Data": "data/sentiment_data.csv"
}
selected_csv = st.selectbox("Select Data File", list(csv_files.keys()))

try:
    df = pd.read_csv(csv_files[selected_csv])
    st.success(f"Loaded {len(df):,} rows from {selected_csv}")
    st.dataframe(df.head(50))
except Exception as e:
    st.error(f"Error loading file: {e}")

# Interactive Pie Charts for Demographics
st.markdown("""
#### Employee Distribution by Demographics
""")
try:
    col1, col2 = st.columns(2)
    with col1:
        fig_gender = px.pie(
            df,
            names="Gender",
            title="Employee Distribution by Gender"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
        fig_tenure = px.pie(
            df,
            names="TenureType",
            title="Employee Distribution by Tenure Type"
        )
        st.plotly_chart(fig_tenure, use_container_width=True)
    with col2:
        fig_dept = px.pie(
            df,
            names="Department",
            title="Employee Distribution by Department"
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        fig_age = px.pie(
            df,
            names="AgeGroup",
            title="Employee Distribution by Age Group"
        )
        st.plotly_chart(fig_age, use_container_width=True)
except Exception as e:
    st.warning(f"Could not load demographic charts: {e}")

# 2. Interactive Pie Charts from task 2.3.ipynb
st.header("Cost & ROI Analysis Visuals")
try:
    merged_costs = pd.read_csv("data/cost_analysis.csv")

    # Pie chart: Benefit Cost Distribution by SubType
    fig1 = px.pie(
        merged_costs,
        values="BenefitCost",
        names="BenefitSubType",
        hover_data=["BenefitType","BenefitSubType","BenefitCost"],
        title="Benefit Cost Distribution by SubType"
    )
    fig1.update_traces(hovertemplate="<b>%{label}</b><br>Cost: $%{value:,.2f}<br>Type: %{customdata[0]}")

    # Pie chart: Benefit Cost Distribution by Benefit Type
    benefit_type_costs = merged_costs.groupby("BenefitType", as_index=False)["BenefitCost"].sum()
    fig2 = px.pie(
        benefit_type_costs,
        values="BenefitCost",
        names="BenefitType",
        hover_data=["BenefitCost"],
        title="Benefit Cost Distribution by Benefit Type"
    )
    fig2.update_traces(hovertemplate="<b>%{label}</b><br>Total Cost: $%{value:,.2f}")

    # Pie chart: Retirement Plan - Cost Distribution by SubType
    retirement_df = merged_costs[merged_costs["BenefitType"] == "Retirement Plan"]
    retirement_costs = retirement_df.groupby("BenefitSubType", as_index=False)["BenefitCost"].sum()
    fig3 = px.pie(
        retirement_costs,
        values="BenefitCost",
        names="BenefitSubType",
        hover_data=["BenefitCost"],
        title="Retirement Plan - Cost Distribution by SubType"
    )
    fig3.update_traces(hovertemplate="<b>%{label}</b><br>Cost: $%{value:,.2f}")

    # Pie chart: Gym Membership - Cost Distribution by SubType
    gym_df = merged_costs[merged_costs["BenefitType"] == "Gym Membership"]
    gym_costs = gym_df.groupby("BenefitSubType", as_index=False)["BenefitCost"].sum()
    fig4 = px.pie(
        gym_costs,
        values="BenefitCost",
        names="BenefitSubType",
        hover_data=["BenefitCost"],
        title="Gym Membership - Cost Distribution by SubType"
    )
    fig4.update_traces(hovertemplate="<b>%{label}</b><br>Cost: $%{value:,.2f}")

    # Display in 2x2 grid
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)
except Exception as e:
    st.warning(f"Could not load interactive charts: {e}")

# 4. Display only bar chart images from images folder in a grid
st.header("All Bar Chart Images from Images Folder")
image_files = [f for f in glob.glob("images/**/*.png", recursive=True) if "bar" in os.path.basename(f).lower()]
if image_files:
    ncols = 3
    rows = [image_files[i:i+ncols] for i in range(0, len(image_files), ncols)]
    for row in rows:
        cols = st.columns(ncols)
        for col, img_path in zip(cols, row):
            with col:
                st.image(Image.open(img_path), use_container_width=True)
else:
    st.info("No bar chart images found in images folder.")

# 2. Show images from task 2.3.ipynb (all 4 images)
image_dir = "images/task_2_3/"
task_images = ["roi_quadrant.png", "cost_histogram.png", "cost_boxplot.png", "roi_histogram.png"]
for img_name in task_images:
    img_path = os.path.join(image_dir, img_name)
    if os.path.exists(img_path):
        st.image(Image.open(img_path), use_container_width=True)

# 3. Show Global KMeans image from ml_clustering.ipynb
global_kmeans_img = "images/ml_clustering/global_kmeans_labeled.png"
if os.path.exists(global_kmeans_img):
    st.image(Image.open(global_kmeans_img), use_container_width=True)

# Display only the specified images in a grid
st.header("Selected Images Grid")
specified_images = [
    "images/401k_dept.png",
    "images/cert_age.png",
    "images/cert_dept.png",
    "images/grad_age.png",
    "images/grad_dept.png",
    "images/infant_dept.png",
    "images/infantcare_usage_gender.png",
    "images/ppo_age.png",
    "images/ppo_dept.png",
    "images/ppo_gender.png",
    "images/transit_dept.png",
    "images/transit_gender.png"
]
existing_images = [img for img in specified_images if os.path.exists(img)]
if existing_images:
    ncols = 3
    rows = [existing_images[i:i+ncols] for i in range(0, len(existing_images), ncols)]
    for row in rows:
        cols = st.columns(ncols)
        for col, img_path in zip(cols, row):
            with col:
                st.image(Image.open(img_path), use_container_width=True)
else:
    st.info("No specified images found.")

# Clustering Images Section
st.header("Clustering Visuals")
clustering_images = [
    "images/boomer_knn.png",
    "images/genx_knn.png",
    "images/genz_kmeans.png",
    "images/gmm.png",
    "images/kmeans.png",
    "images/kmeans_millenial.png"
]
existing_clustering_images = [img for img in clustering_images if os.path.exists(img)]
if existing_clustering_images:
    ncols = 3
    rows = [existing_clustering_images[i:i+ncols] for i in range(0, len(existing_clustering_images), ncols)]
    for row in rows:
        cols = st.columns(ncols)
        for col, img_path in zip(cols, row):
            with col:
                st.image(Image.open(img_path), use_container_width=True)
else:
    st.info("No clustering images found.")
