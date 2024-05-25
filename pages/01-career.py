import pandas as pd
import numpy as np
import streamlit as st
import random
import ahp
import ahp_ui


all_weights = {}
categories = {
    "Barriers to Entry": ["Unemployment rate", "Higher education requirements", "Difficulty", "Competitiveness"],
    "Quality of Life": ["Work-life balance", "Geographic mobility", "Altruism", "Physical demands"],
    "Outcomes": ["Entry-level salary", "Career growth potential", "Average debt load"],
}

st.write("## Categories")
st.write(f"Career choice has been broken down into {len(categories)} categories: {', '.join(categories)}. As you adjust your preferences the percentage allocated to each category automatically update.")
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
    dict([("name", "Accountant")] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
    dict([("name", "Dentist")] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
    dict([("name", "Elementary school teacher")] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
    dict([("name", "Lawyer")] + [(i, random.randrange(10)) for k, v in categories.items() for i in v]),
]

df = pd.DataFrame([(a['name'], ahp.utility(categories, all_weights, a)) for a in dummy_alts], columns=['Name', 'Score',]).sort_values('Score', ascending=False)
st.dataframe(df, hide_index=True)
