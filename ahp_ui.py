import streamlit as st
import numpy as np
import pandas as pd
import ahp


def draw_weight_sliders(categories):
    with st.expander("Pairwise criteria comparisons for all categories"):
        st.write("Which is more important?")
        m = np.eye(len(categories))
        for i, a in enumerate(categories):
            for j, b in enumerate(categories):
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
    return pd.DataFrame(np.concatenate((labels, weights.reshape(-1, 1)), axis=1), columns=['item', 'weights',])
