import pandas as pd
import numpy as np
import streamlit as st
import random
import ahp


# TODO: user input criteria in N categories
# Filter by specific degree programs
# Define preferences for location, i.e. is close to home good or bad
# Quality (rankings by program, teacher:student ratios, admission rate), location (weather, distance from home, city vs rural), student outcomes (job placement rate, graduation rate)
# TODO: nested criteria and propogation
# TODO: alternatives input & evaluation

all_weights = {}
categories = {
    "Quality": ["University ranking", "Field ranking", "Undergraduate research opportunities", "Student-teacher ratio", "Admission rates"],
    "Geography": ["Urban or rural", "Weather", "Distance from home"],
    "Outcomes": ["Job placement rate", "4-year graduation rate", "Average debt load"],
    "Extracurriculars": ["University athletics division", "University athletics ranking", "Volunteering opportunities"],
}

st.write("## Introduction")
st.write("This application is designed to help apply rigor to weighty decisions for your average Joe. This is done via the [Analytic Hierarchy Process (AHP)](https://en.wikipedia.org/wiki/Analytic_hierarchy_process), using pairwise comparisons of categories & criteria to derive a unique utility function for each topic.")
st.write("There are currently 2 demos of this process in action. The first for career selection:")
st.page_link("pages/01-career.py")
st.write("And the second for undergraduate school selection:")
st.page_link("pages/02-school.py")

st.write("These categories are currently fixed, but each one has multiple criteria within it that you will select. For each category, as well as the criteria within the category, you will be asked to compare all permutations of pairs within that list. You need to adjust the sliders to move closer to the option you prefer. For example, using the same method for this question:")

st.write("Which is more important?")
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.write("Speed")
with col2:
    ex_slider = st.slider("Speed vs Endurance", -8, 8, 0, 1, label_visibility="collapsed")
with col3:
    st.write("Endurance")

st.write("Your selection is telling us that:")
if ex_slider < -5:
    st.write("Speed is MUCH more important to you!")
elif ex_slider < -1:
    st.write("Speed is somewhat more important to you.")
elif ex_slider <= 1:
    st.write("Speed and Endurance are roughly equal in importance to you.")
elif ex_slider <= 5:
    st.write("Endurance is somewhat more important to you.")
else:
    st.write("Endurance is MUCH more important to you!")

st.write('There is also a "consistency check" in place. This identifies possible circular logic that would make it impossible to accurately quantify. For instance, a class rock-paper-scissors result in a pairwise comparison would make no sense, as it is impossible to determine which result is "better".')

st.write('Once we have all of these results we can evaluate all the categories & criteria to build the weights for your personal "utility function". This function can then be used to evaluate candidate alternatives to derive a "score" for each one, which should help you balance the overall value (or utility) against the costs.')