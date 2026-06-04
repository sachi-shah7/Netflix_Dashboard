import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import base64

df = pd.read_excel("netflix_titles.csv.xlsx")   #add data

st.set_page_config(page_title="Netflix Analytics", layout="wide")

data = base64.b64encode(open("bg1.jpg", "rb").read()).decode()

st.sidebar.markdown("""
    <style>
    .sidebar-title {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #E50914; /* Netflix Red */
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    </style>
    <p class="sidebar-title">ANALYSIS</p>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Choose:",["Home", "Data Overview", "Content Analysis","Global Analysis","Rating Distribution","Genre Analysis","Movie Durations"])

if page == "Home":
    st.markdown(f"""
    <style>
    .stApp {{ background: url("data:image/png;base64,{data}") center/cover; }}
    .main-container {{ display: flex; justify-content: center; align-items: center; height: 80vh; }}
    .n-box {{ background: rgba(0,0,0,0.85); padding: 40px 60px; border-radius: 15px; border-top: 8px solid #E50914; text-align: center; }}
    h1 {{ color: white !important; font-size: 70px; margin: 0; font-weight: bold; }}
    </style>
    <div class="main-container"><div class="n-box"><h1>NETFLIX <span style="color: #E50914;">DATA ANALYSIS</span></h1></div></div>
    """, unsafe_allow_html=True)

elif page == "Data Overview":
    # 1. Netflix Styling
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] { color: #E50914 !important; font-size: 50px !important; font-weight: bold; }
        .netflix-title { border-left: 6px solid #E50914; padding-left: 15px; margin-bottom: 25px; }
        </style>
        <div class="netflix-title"><h1> Data Overview</h1></div>
    """, unsafe_allow_html=True)

    # 2. Table Section
    st.write("The first 10 data contents are as follows:")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True) # Space

    # 3. Metrics Section (Totals)
    c1, c2, c3 = st.columns(3)
    counts = df['Type'].value_counts()
    
    c1.metric("Total", len(df))
    c2.metric("Movies", counts.get('Movie', 0))
    c3.metric("TV Shows", counts.get('TV Show', 0))

    st.write("The **Netflix Data Analysis** reveals a library structure that prioritizes volume and variety to maintain its position as a global streaming leader. With a total of *8,807 titles*, the dataset highlights a significant skew toward standalone cinematic content. Movies account for *6,131* of the entries, representing nearly *70 percent* of the entire database. This indicates that while binge-watching TV series is a major part of the platform's marketing, the backbone of its catalog remains fixed-length films, which likely offer lower production costs per title compared to multi-season series.")
    st.write("A standout metric is the *514 Unique Genres*. This high number suggests that Netflix uses a highly granular tagging system rather than broad categories. By combining labels like *International TV Shows*, *Crime TV Shows*, and *South African*, the platform creates niche micro-genres. This strategy is evident in the Dataset Preview, where titles from South Africa, India, and the United Kingdom appear in the first ten rows alone. This geographical diversity, paired with the variety of ratings from PG-13 to TV-MA, shows a platform that is intentionally moveing away from a one-size-fits-all model. Instead, it is curated to satisfy highly specific cultural and age demographics simultaneously, using its vast movie library to provide immediate variety while leveraging a smaller, more focused collection of TV Shows for long-term subscriber engagement.")

elif page == "Content Analysis":
    # 1. Matching Vertical Red Border Heading
    st.markdown("""
        <div style="border-left: 8px solid #E50914; padding-left: 15px; margin-bottom: 20px;">
            <h1 style="color: #221f1f; margin: 0; font-size: 38px;"> Content Analysis</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. Data & Plot
    td = df[df['Date Released'] >= 1940].groupby(['Date Released', 'Type']).size().reset_index(name='n')
    
    fig = px.line(td, x="Date Released", y="n", color="Type", markers=True,
                  color_discrete_map={"Movie": "#221f1f", "TV Show": "#E50914"})

    # 3. Clean Layout
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=20, b=10),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Year"),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Titles"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.write("The **Content Analysis** reveals a dramatic shift in Netflix’s strategy over the last century. While the library includes rare cinematic gems dating back to 1925, there is an exponential explosion in volume starting around 2015, marking the platform's transition into a global production powerhouse.")
    st.write("The data shows a clear dominance of **Movies**, which reached a massive production peak between **2017** and **2018**. However, **TV Shows** have exhibited a more consistent and resilient growth trajectory into the **2020s**. This suggests a strategic pivot toward serialized storytelling to drive long-term subscriber retention, catering to the modern binge-watching habits of the digital age.")

elif page == "Global Analysis":
    st.markdown("""
        <div style="border-left: 8px solid #E50914; padding-left: 15px; margin-bottom: 20px;">
            <h1 style="color: #221f1f; margin: 0; font-size: 38px;"> Where is Netflix content coming from?</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. Quick Data Prep
    countries = df['Country'].str.split(',').str[0].value_counts().reset_index()
    countries.columns = ['Country', 'Count']

    # 2. Optimized Netflix-style Map
    fig = px.choropleth(countries, locations="Country", locationmode='country names', 
                        color="Count", hover_name="Country",
                        color_continuous_scale="Blues") # Light gray to Netflix Red

    fig.update_layout(
        height=600, margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular')
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. Top 10 Table
    st.subheader("Top 10 Producers")
    st.table(countries.head(10))

    st.write("The table of **Top 10 Producers** highlights a significant concentration of content production, with the United States leading by a massive margin at 3,211 titles. India holds a strong second place with 1,008 titles, establishing itself as a primary hub for international content. The United Kingdom (628) and Canada (271) follow, showcasing the platform's reliance on English-speaking markets. Meanwhile, the presence of Japan (259) and South Korea (211) reflects the growing global popularity of anime and K-dramas. Overall, these nations represent a diverse mix of global cinematic powerhouses, illustrating Netflix's strategy of balancing Hollywood blockbusters with regional specialties.")

elif page == "Rating Distribution":
    # 1. Signature Vertical Red Border Heading
    st.markdown('<div style="border-left: 8px solid #E50914; padding-left: 15px; margin-bottom: 20px;"><h1 style="color: #221f1f; margin: 0; font-size: 38px;"> Rating Distribution</h1></div>', unsafe_allow_html=True)

    # 2. Data: Get Top 10 Ratings
    rating_counts = df['Rating'].value_counts().head(10).reset_index()
    rating_counts.columns = ['Rating', 'Count']

    # 3. Interactive Bar Chart
    fig = px.bar(rating_counts, x='Rating', y='Count', 
                 text_auto=True,
                 color_discrete_sequence=['#E50914']) # Netflix Red

    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="Ratings", yaxis_title="Number of Titles",
        margin=dict(t=10, b=10, l=0, r=0)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4. Brief Analysis
    st.write("This chart displays the top 10 most common content ratings. **TV-MA** and **TV-14** typically dominate, reflecting Netflix's focus on adult and teen audiences. Together, these two categories dwarf the rest of the distribution, indicating a primary strategic focus on adult and teenage demographics. In contrast, family-oriented or general audience ratings like TV-G and NR (Not Rated) sit at the bottom of the top 10, with fewer than 220 titles each. The sharp decline in volume after the first two categories suggests that while the library is diverse, its heavy hitters are concentrated in restricted or guided viewing tiers.")

elif page == "Genre Analysis":
    st.markdown('<div style="border-left: 8px solid #E50914; padding-left: 15px; margin-bottom: 20px;"><h1 style="color: #221f1f; margin: 0; font-size: 38px;"> Genre Evolution</h1></div>', unsafe_allow_html=True)

    # 1. Prepare Data: Split and Explode
    genre_df = df.copy()
    genre_df['Listed In'] = genre_df['Listed In'].str.split(', ')
    genre_df = genre_df.explode('Listed In')
    
    # 2. Focus on Top 10 Genres since 2010
    top_10 = genre_df['Listed In'].value_counts().nlargest(10).index
    genre_trend = genre_df[genre_df['Listed In'].isin(top_10)]
    genre_trend = genre_trend.groupby(['Date Released', 'Listed In']).size().reset_index(name='Count')
    genre_trend = genre_trend[genre_trend['Date Released'] >= 2010]

    # 3. Plot
    fig = px.area(genre_trend, x="Date Released", y="Count", color="Listed In",
                  title="Top 10 Genres Over Time",
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    
    st.plotly_chart(fig, use_container_width=True)

    st.write("The Genre Evolution chart illustrates a dramatic transformation in content production and acquisition, characterized by a massive surge in volume starting around 2015. Prior to this period, the library maintained a relatively flat and modest distribution across all categories. However, the mid-2010s marked a clear pivot toward aggressive expansion, with the total count of titles peaking around 2018 before experiencing a visible decline as the timeline approaches 2021.")

    st.write("A closer look at the stacked layers reveals that **International Movies** and **Dramas** emerged as the primary engines of this growth, occupying the largest surface area on the graph. The widening bands for International TV Shows and International Movies suggest a strategic shift toward a globalized content library, likely aimed at capturing diverse markets outside of domestic audiences. While categories like Documentaries and Comedies grew in absolute numbers, they remained secondary to the dominant scripted drama and international categories.")

elif page == "Movie Durations":
    st.markdown("""
        <div style="border-left: 8px solid #E50914; padding-left: 15px; margin-bottom: 20px;">
            <h1 style="color: #221f1f; margin: 0; font-size: 38px;">Movie Duration Trends</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. CREATE THE DATAFRAME FIRST (Crucial Step)
    # We filter for Movies and convert duration strings to integers
    m_df = df[df['Type'] == 'Movie'].copy()
    m_df['Mins'] = m_df['Duration'].str.replace(' min', '', regex=False).fillna('0').astype(int)
    m_df = m_df[m_df['Mins'] > 0] # Remove any 0 min entries

    # 3. NOW create the chart using the m_df we just made
    fig = px.scatter(m_df, x="Date Released", y="Mins", trendline="ols",
                     hover_name="Title", render_mode="webgl", 
                     color_discrete_sequence=['#28a745'], opacity=0.4)
    st.plotly_chart(fig, use_container_width=True)

    # 4. NOW the Fun Fact (m_df is now guaranteed to exist)
    shortest = m_df.sort_values('Mins').iloc[0]
    st.info(f"💡 **Fun Fact:** The shortest movie is **'{shortest['Title']}'** ({shortest['Mins']} min)!")

    # 5. Analysis text
    st.write("The downward-sloping trend line confirms that **movies are getting shorter**, clustering around the 90–110 minute mark to suit modern streaming habits.This reflects an industry-wide move toward tighter editing and streaming-optimized durations. Despite this, the dataset still captures occasional 3-hour+ outliers, showing that long-form storytelling remains a key part of the library")

