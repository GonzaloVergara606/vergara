mport streamlit as st
import pandas as pd
import plotly.express as px

# Load data
st.title("Gonzalo Vergara")

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = df.rename(columns={"room_type": "listing_type", "neighbourhood": "neighborhood"})
        df.dropna(subset=["price"], inplace=True)  # Remove rows without price
        return df
    return None

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
df = load_data(uploaded_file)

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    listing_types = st.sidebar.multiselect("Select listing types", df["listing_type"].unique(), default=df["listing_type"].unique())
    neighborhoods = st.sidebar.multiselect("Select neighborhoods", df["neighborhood"].unique(), default=df["neighborhood"].unique())
    filtered_df = df[(df["listing_type"].isin(listing_types)) & (df["neighborhood"].isin(neighborhoods))]

    # Tabs
    tab1, tab2 = st.tabs(["Analysis", "Simulator"])

    # Analysis Tab
    with tab1:
        col1, col2 = st.columns(2)
        
        # Chart 1: Minimum nights by listing type
        with col1:
            fig1 = px.box(filtered_df, x="listing_type", y="minimum_nights", title="Minimum nights by listing type")
            st.plotly_chart(fig1)
        
        # Chart 2: Price by listing type
        with col2:
            fig2 = px.box(filtered_df, x="listing_type", y="price", title="Price by listing type")
            st.plotly_chart(fig2)
        
        # Chart 3: Most reviewed apartments per month by neighborhood
        top_reviews = filtered_df.groupby(["neighborhood", "listing_type"]).agg({"reviews_per_month": "sum"}).reset_index()
        fig3 = px.bar(top_reviews, x="neighborhood", y="reviews_per_month", color="listing_type", title="Most reviewed apartments per month by neighborhood")
        st.plotly_chart(fig3)
        
        # Chart 4: Relationship between reviews and price
        fig4 = px.scatter(filtered_df, x="number_of_reviews_ltm", y="price", color="listing_type", title="Reviews vs Price")
        st.plotly_chart(fig4)
        
        # Chart 5: Availability vs Price
        fig5 = px.scatter(filtered_df, x="availability_365", y="price", color="listing_type", title="Availability vs Price")
        st.plotly_chart(fig5)

    # Price Simulator Tab
    with tab2:
        st.header("Price Simulator")
        selected_neighborhood = st.selectbox("Select a neighborhood", df["neighborhood"].unique())
        selected_type = st.selectbox("Select listing type", df["listing_type"].unique())
        num_nights = st.slider("Number of nights", 1, 30, 2)
        
        # Filter similar listings
        similar_listings = df[(df["neighborhood"] == selected_neighborhood) & (df["listing_type"] == selected_type) & (df["minimum_nights"] >= num_nights)]
        price_range = (similar_listings["price"].quantile(0.25), similar_listings["price"].quantile(0.75))
        
        st.write(f"Recommended price range: ${price_range[0]:.2f} - ${price_range[1]:.2f}")

# Instructions
st.sidebar.markdown("## Instructions")
st.sidebar.info("Upload this code to Streamlit Cloud and submit the link on Moodle.")
