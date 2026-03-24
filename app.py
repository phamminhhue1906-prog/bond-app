import streamlit as st
import pandas as pd

st.title("Bond Yield Interpolation Tool")

file = st.file_uploader("Upload your yield data", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    df.columns = ['tenor', 'yield', 'bid', 'ask', 'spread']
    df = df.sort_values(by='tenor')

    tenors = df['tenor'].values
    yields = df['yield'].values
    bids   = df['bid'].values
    asks   = df['ask'].values

    def interpolate(m, tenors, values):
        for i in range(len(tenors)-1):
            x1, x2 = tenors[i], tenors[i+1]
            if x1 <= m <= x2:
                y1, y2 = values[i], values[i+1]
                return y1 + (m-x1)*(y2-y1)/(x2-x1)

    m = st.slider("Select tenor", 1.0, 30.0, 10.0)

    y = interpolate(m, tenors, yields)
    b = interpolate(m, tenors, bids)
    a = interpolate(m, tenors, asks)

    st.write(f"### Results for {m}Y")
    st.write(f"Yield: {y*100:.3f}%")
    st.write(f"Bid:   {b*100:.3f}%")
    st.write(f"Ask:   {a*100:.3f}%")

    spread = (b - a) * 10000
    st.write(f"Spread: {spread:.1f} bps")
