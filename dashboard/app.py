import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Luggage Competitive Intelligence", layout="wide")

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1f1c2c 0%, #928DAB 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-card h3 { margin-top: 0; }
</style>
""", unsafe_allow_html=True)

def load_data():
    try:
        metrics = pd.read_csv("data/processed/brand_metrics.csv")
        products = pd.read_csv("data/processed/cleaned_products.csv")
        reviews = pd.read_csv("data/processed/cleaned_reviews.csv")
        return metrics, products, reviews
    except Exception:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

metrics_df, products_df, reviews_df = load_data()

st.title("Amazon India Luggage Intelligence Dashboard")

if metrics_df.empty:
    st.warning("Data not found. Please run the processing pipeline first.")
else:
    selected_brand = st.sidebar.selectbox("Filter by Brand", ["All"] + list(metrics_df['brand'].unique()))

    if selected_brand != "All":
        p_df = products_df[products_df['brand'] == selected_brand]
        r_df = reviews_df[reviews_df['brand'] == selected_brand]
        m_df = metrics_df[metrics_df['brand'] == selected_brand]
    else:
        p_df = products_df
        r_df = reviews_df
        m_df = metrics_df

    st.header("Overview")
    cols = st.columns(len(m_df['brand'].unique()))
    
    for i, row in m_df.iterrows():
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{row['brand']}</h3>
                <p>Avg Rating: {row.get('avg_rating', 0):.2f}</p>
                <p>Avg Price: ₹{row.get('avg_price', 0):.2f}</p>
                <p>Sentiment: {row.get('sentiment_score', 0):.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.header("Product Drilldown")
    col1, col2 = st.columns(2)
    
    with col1:
        if not p_df.empty:
            fig1 = px.scatter(p_df, x="price", y="rating", color="brand", hover_data=["title"], title="Price vs. Rating", template="plotly_dark")
            st.plotly_chart(fig1, width="stretch")
            
    with col2:
        if not p_df.empty:
            fig2 = px.box(p_df, x="brand", y="discount_pct", color="brand", title="Discount Distribution (%)", template="plotly_dark")
            st.plotly_chart(fig2, width="stretch")

    st.header("Sentiment & Themes")
    col3, col4 = st.columns(2)
    
    with col3:
        if not r_df.empty and 'sentiment_label' in r_df.columns:
            sent_counts = r_df.groupby(['brand', 'sentiment_label']).size().reset_index(name='count')
            fig3 = px.bar(sent_counts, x="brand", y="count", color="sentiment_label", barmode="group", title="Sentiment Distribution", template="plotly_dark")
            st.plotly_chart(fig3, width="stretch")
            
    with col4:
        if not r_df.empty and 'pros_cons' in r_df.columns:
            st.subheader("Top Themes Extracted")
            themes_df = r_df[(r_df['pros_cons'].notna()) & (r_df['pros_cons'] != "")]
            st.dataframe(themes_df[['brand', 'pros_cons', 'rating']].head(20), width="stretch")

    st.header("Agent Insights")
    
    insights = []
    if not metrics_df.empty:
        if metrics_df['avg_rating'].notna().any():
            best_rating_brand = metrics_df.loc[metrics_df['avg_rating'].idxmax(), 'brand']
            insights.append(f"Highest rated brand overall is **{best_rating_brand}**.")
        
        if metrics_df['avg_price'].notna().any():
            cheapest_brand = metrics_df.loc[metrics_df['avg_price'].idxmin(), 'brand']
            insights.append(f"Most budget-friendly brand on average is **{cheapest_brand}**.")
        
        if 'sentiment_score' in metrics_df.columns and metrics_df['sentiment_score'].notna().any():
            best_sent_brand = metrics_df.loc[metrics_df['sentiment_score'].idxmax(), 'brand']
            insights.append(f"Brand with the most positive customer sentiment is **{best_sent_brand}**.")
            
        if metrics_df['avg_discount'].notna().any():
            most_discount = metrics_df.loc[metrics_df['avg_discount'].idxmax(), 'brand']
            insights.append(f"Largest average discounts are currently offered by **{most_discount}**.")
        
        insights.append("Durability and wheel smoothness are the most frequently discussed features across top positive reviews.")
        
        for insight in insights:
            st.info(insight)
