import pandas as pd
import numpy as np
import streamlit as st
import random
import ahp
import ahp_ui


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

# st.write("## Personal preferences")
# st.write('In order to calibrate the "direction" of results, we need to clarify some things. For example, if a school is far away from a major metro is that a good thing or a bad thing?')
# urban = st.radio("Do you prefer urban or rural?", ["Urban", "Rural"])
# home = st.radio("Do you prefer to be closer to home or farther away?", ["Close", "Far"])
# degrees = st.multiselect("What degree programs are you interested in?", ["Nursing", "Pre-med", "Pre-law", "Computer science", "Business"])

st.write("## Categories")
st.write(f"School choice has been broken down into {len(categories)} categories: {', '.join(categories)}. As you adjust your preferences the percentage allocated to each category automatically update.")
category_weights = ahp_ui.foo(categories.keys())
for idx, category in enumerate(categories.keys()):
    all_weights[category] = float(category_weights[category_weights['item'] == category].weights[idx])

for category, criteria_options in categories.items():
    st.write(f"### {category} ({all_weights[category]:.1%})")
    criteria = st.multiselect(label="Please select the criteria that are important to you", options=criteria_options, key=category)
    if len(criteria) > 0:
        final = ahp_ui.foo(criteria)
        for idx, c in enumerate(criteria):
            all_weights[c] = float(final[final['item'] == c].weights[idx])

st.write("### Utility function")
with st.expander("Beware, here lies more math"):
    st.write("The general definition of the utility function is as follows, where `k` is each category and `j` is each criteria within that category, with `w` representing the weights and `v` representing the relative value for that criteria for a given candidate:")
    st.latex(r'''
            U = \sum_{k=0}^{n} w_k \sum_{j=0}^{m} w_j v_j
        ''')
    st.write("Here is your personalized utility function based on your selections:")
    utility_function_str = "Utility = "
    for cat, child in categories.items():
        utility_function_str += f"\n+ ({all_weights[cat]:0.3f} * ("
        for i in child:
            utility_function_str += f"\n\t+ ({all_weights[i] if i in all_weights else 0:0.3f} * [{i}])"
        utility_function_str += "))"
    st.code(utility_function_str)

st.write("## Results")
st.write("For now I have just populated some dummy data to showcase the general process. This should be updated with a whole additional process of data collection & normalization. This may impact the categories & criteria eligible for selection depending on what data is available.")
random.seed(777)
dummy_alts = [
    dict([("name", "City U"), ("tuition", 10_000)] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
    dict([("name", "U of A"), ("tuition", 20_000)] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
    dict([("name", "U of B"), ("tuition", 30_000)] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
    dict([("name", "College University of Schooltown, Minnesota"), ("tuition", 40_000)] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
]

df = pd.DataFrame([(a['name'], a['tuition'], ahp.utility(categories, all_weights, a), ahp.utility(categories, all_weights, a)/a['tuition']*1_000) for a in dummy_alts], columns=['Name', 'Tuition', 'Score', 'Bang per buck',]).sort_values('Bang per buck', ascending=False)
st.dataframe(df, hide_index=True)
