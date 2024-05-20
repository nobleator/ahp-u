import pandas as pd
import numpy as np
import streamlit as st
import random
# import streamlit_mermaid as stmd
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
st.write('This application is designed to help you select a university by evaluating each candidate school against quantifiable measurements of your preferences. This process starts with you breaking down your unique preferences by comparing criteria against each other in a "pairwise comparison".')
st.write(f"I have broken this down into {len(categories)} categories: {', '.join(categories)}")

# graph = "graph TD"
# node_ctr = 0
# for k, v in categories.items():
#     graph += f"\n    Utility --- {k}"
#     # for c in v:
#     #     graph += f"\n    {k} --- {node_ctr}[{c}]"
#     #     node_ctr += 1
# stmd.st_mermaid(graph)

st.write("These categories are currently fixed, but each one has multiple criteria within it that you will select. For each category, as well as the criteria within the category, you will be asked to compare all perumutations of pairs within that list. You need to adjust the sliders to move closer to the option you prefer. For example, using the same method for this question:")
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

# st.write('There is also a "consistency check" in place. This identifies possible circular logic that would make it impossible to accurately quantify. For instance, a class rock-paper-scissors result in a pairwise comparison would make no sense, as it is impossible to determine which result is "better".')

st.write('Once we have all of these results we can evaluate all the categories & criteria to build the weights for your personal "utility function". This function can then be used to evaluate candidate schools to derive a "score" for each one, which should help you balance the overall value (or utility) against the costs of attendance.')

# st.write("## Personal preferences")
# st.write('In order to calibrate the "direction" of results, we need to clarify some things. For example, if a school is far away from a major metro is that a good thing or a bad thing?')
# urban = st.radio("Do you prefer urban or rural?", ["Urban", "Rural"])
# home = st.radio("Do you prefer to be closer to home or farther away?", ["Close", "Far"])
# degrees = st.multiselect("What degree programs are you interested in?", ["Nursing", "Pre-med", "Pre-law", "Computer science", "Business"])

st.write("## Categories")
st.write("Now we can dive into the categories. As you adjust your preferences the percentage allocated to each category automatically update.")
with st.expander("Pairwise criteria comparisons for all categories"):
    st.write("Which is more important?")
    m = np.eye(len(categories.keys()))
    for i, a in enumerate(categories.keys()):
        for j, b in enumerate(categories.keys()):
            if j <= i:
                continue
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.write(a)
            with col2:
                raw_val = st.slider(f'Is "{a}" more important than "{b}"?', -8, 8, 0, 1, key=f"categories_{a}_{b}", label_visibility="collapsed")
            with col3:
                st.write(b)
            m[i,j] = 1 if raw_val == 0 else -raw_val+1 if raw_val < 0 else 1/(raw_val+1)
weights = ahp.get_weights(m)
if ahp.check_consistency(m, weights) > 0.1:
    st.write("Warning, check your inputs for consistency!")
labels = np.array(list(categories)).reshape(-1, 1)
category_weights = pd.DataFrame(np.concatenate((labels, weights.reshape(-1, 1)), axis=1), columns=['category', 'weights',])
for idx, category in enumerate(categories.keys()):
    all_weights[category] = float(category_weights[category_weights['category'] == category].weights[idx])

for category, criteria_options in categories.items():
    st.write(f"### {category} ({all_weights[category]:.1%})")
    criteria = st.multiselect(label="Please select the criteria that are important to you", options=criteria_options, key=category)
    if len(criteria) > 0:
        with st.expander(f"Pairwise criteria comparisons for {category}"):
            st.write("Which is more important?")
            m = np.eye(len(criteria))
            for i, a in enumerate(criteria):
                for j, b in enumerate(criteria):
                    if j <= i:
                        continue
                    col1, col2, col3 = st.columns([1, 4, 1])
                    with col1:
                        st.write(a)
                    with col2:
                        raw_val = st.slider(f'Is "{a}" more important than "{b}"?', -8, 8, 0, 1, key=f"{category}_{a}_{b}", label_visibility="collapsed")
                    with col3:
                        st.write(b)
                    m[i,j] = 1 if raw_val == 0 else -raw_val+1 if raw_val < 0 else 1/(raw_val+1)
        weights = ahp.get_weights(m)
        if ahp.check_consistency(m, weights) > 0.1:
            st.write("Warning, check your inputs for consistency!")
        labels = np.array(criteria).reshape(-1, 1)
        final = pd.DataFrame(np.concatenate((labels, weights.reshape(-1, 1)), axis=1), columns=['criteria', 'weights',])
        for idx, c in enumerate(criteria):
            all_weights[c] = float(final[final['criteria'] == c].weights[idx])

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

def utility(categories: dict[str, list[str]], weights: dict[str, float], candidate):
    total = 0
    for c, cr in categories.items():
        sub = 0
        for x in cr:
            sub += (candidate[x] * weights[x] if x in weights else 0)
        total += sub * weights[c]
    return total

df = pd.DataFrame([(a['name'], a['tuition'], utility(categories, all_weights, a), utility(categories, all_weights, a)/a['tuition']*1_000) for a in dummy_alts], columns=['Name', 'Tuition', 'Score', 'Bang per buck',]).sort_values('Bang per buck', ascending=False)
st.dataframe(df, hide_index=True)
