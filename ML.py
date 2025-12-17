import streamlit as st
import pandas as pd
from datetime import datetime


#Data 


import random

first_names = ["Alice", "Brian", "Clara", "David", "Elena", "Frank", "Grace", "Henry", "Isha", "James", "Klara", "Liam", "Maya", "Noah", "Olivia"]
last_names = ["Morgan", "Patel", "Schmidt", "Rossi", "Nguyen", "Brown", "Taylor", "Meier", "Singh", "Clark"]

titles = [
    "Director of Toxicology",
    "Head of Safety Assessment",
    "VP Preclinical Safety",
    "Senior Scientist",
    "Junior Scientist",
    "Principal Toxicologist"
]

companies = ["HepatoBio", "LiverTech", "OncoSafety", "PreClinica", "ToxiCore", "BioSphere"]

locations = [
    ("Boston, MA", "Cambridge, MA"),
    ("San Francisco, CA", "Bay Area, CA"),
    ("Basel, Switzerland", "Basel, Switzerland"),
    ("Oxford, UK", "Oxford, UK"),
    ("Austin, TX", "Austin, TX")
]

funding_stages = ["Bootstrapped", "Series A", "Series B", "IPO"]

publications = [
    ("Drug-Induced Liver Injury in 3D Hepatic Models", 2024),
    ("Organ-on-Chip Approaches for Toxicology", 2023),
    ("Investigative Toxicology Methods", 2022),
    ("Cell Viability Assays", 2021)
]

data = []

for i in range(15):
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    title = random.choice(titles)
    company = random.choice(companies)
    personal_loc, hq = random.choice(locations)
    funding = random.choice(funding_stages)
    pub_title, pub_year = random.choice(publications)
    uses_invitro = "3D" in pub_title or "Organ" in pub_title

    data.append({
        "Name": f"Dr. {fname} {lname}",
        "Title": title,
        "Company": company,
        "Personal_Location": personal_loc,
        "Company_HQ": hq,
        "Funding": funding,
        "Publication": pub_title,
        "Publication_Year": pub_year,
        "Uses_InVitro": uses_invitro,
        "Email": f"{fname.lower()}.{lname.lower()}@{company.lower()}.com",
        "LinkedIn": f"https://linkedin.com/in/{fname.lower()}{lname.lower()}"
    })



# Scoring Engine


def calculate_score(row):
    score = 0

    # Role Fit
    if any(x in row["Title"].lower() for x in ["director", "head", "vp", "toxicology", "safety"]):
        score += 30

    # Funding Intent
    if row["Funding"] in ["Series A", "Series B", "IPO"]:
        score += 20

    # Technographic
    if row["Uses_InVitro"]:
        score += 15

    # Location Hub
    hubs = ["boston", "cambridge", "bay area", "basel", "uk"]
    if any(hub in row["Company_HQ"].lower() for hub in hubs):
        score += 10

    # Scientific Intent
    current_year = datetime.now().year
    if row["Publication_Year"] >= current_year - 2 and "liver" in row["Publication"].lower():
        score += 40

    return min(score, 100)


# Streamlit UI


st.set_page_config(page_title="AI BD Lead Agent", layout="wide")
st.title(" AI Web Agent for Lead Qualification ")
st.caption("3D In-Vitro Models | Toxicology | Safety Assessment")

df = pd.DataFrame(data)
df["Probability_Score"] = df.apply(calculate_score, axis=1)
df = df.sort_values(by="Probability_Score", ascending=False).reset_index(drop=True)
df["Rank"] = df.index + 1

search = st.text_input("Search by location, title, or keyword")
if search:
    df = df[df.apply(lambda row: search.lower() in row.to_string().lower(), axis=1)]

st.dataframe(df[[
    "Rank",
    "Probability_Score",
    "Name",
    "Title",
    "Company",
    "Personal_Location",
    "Company_HQ",
    "Email",
    "LinkedIn"
]], use_container_width=True)

st.download_button(
    label="Export Leads to CSV",
    data=df.to_csv(index=False),
    file_name="ranked_leads_demo.csv",
    mime="text/csv"
)

st.info("This demo simulates LinkedIn, PubMed, and funding intelligence for evaluation purposes.")
