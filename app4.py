import pickle
import streamlit as st
import requests

# Page configuration - MUST be first!
st.set_page_config(
    page_title="🎬 CineMatch - Movie Recommender", 
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme design
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
                
    }
    
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        padding: 2rem;
                            
    }
   
    
    .header-section {
        text-align: center;
        padding: 3rem 0 4rem 0;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        border: 1px solid #333;
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #ff6b6b20, #4ecdc420, #45b7d120, #96ceb420);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        z-index: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 50px rgba(255, 107, 107, 0.5);
        letter-spacing: -2px;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #aaa;
        font-weight: 300;
        letter-spacing: 0.5px;
        margin-bottom: 2rem;
    }
    
    
    
    .search-title {
        # color: #fff;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .stSelectbox > div > div {
        background: #2a2a2a !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        color: #fff !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #ff6b6b !important;
        box-shadow: 0 0 20px rgba(255, 107, 107, 0.3) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #fff !important;
        background: #2a2a2a !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
        width: 100% !important;
        margin-top: 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.6) !important;
        background: linear-gradient(135deg, #ee5a24, #ff6b6b) !important;
    }
    
    .movie-details {
        background: #1a1a1a;
        padding: 3rem;
        border-radius: 20px;
        margin: 3rem 0;
        border: 1px solid #333;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    
    .movie-details h3 {
        color: #ff6b6b;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .movie-poster {
        border-radius: 15px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
        transition: transform 0.3s ease;
        border: 2px solid #333;
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
    }
    
    .movie-info {
        padding-left: 2rem;
    }
    
    .movie-stat {
        background: linear-gradient(135deg, #2a2a2a, #3a3a3a);
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        border-left: 4px solid #ff6b6b;
        color: #fff;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .movie-stat:hover {
        background: linear-gradient(135deg, #3a3a3a, #4a4a4a);
        transform: translateX(5px);
    }
    
    .movie-stat strong {
        color: #ff6b6b;
        font-weight: 600;
    }
    
    .recommendations {
        background: #1a1a1a;
        padding: 3rem;
        border-radius: 20px;
        margin: 3rem 0;
        border: 1px solid #333;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }
    
    .recommendations-title {
        color: #fff;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 3rem;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    } 
    .recommendation-card:hover {
        transform: translateY(-10px);
        border-color: #ff6b6b;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7);
        background: linear-gradient(135deg, #3a3a3a, #2a2a2a);
    }
    
    .recommendation-poster {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6);
        transition: transform 0.3s ease;
        border: 1px solid #404040;
    }
    
    .recommendation-poster:hover {
        transform: scale(1.05);
    }
    
    .recommendation-title {
        color: #fff;
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.4;
        margin-top: 1rem;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff6b6b, transparent);
        border: none;
        margin: 4rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 3rem;
        color: #666;
        font-size: 1rem;
        border-top: 1px solid #333;
        margin-top: 4rem;
    }
    
    .loading {
        text-align: center;
        padding: 3rem;
        color: #ff6b6b;
        font-size: 1.2rem;
    }
    
    .spinner {
        border: 3px solid #333;
        border-top: 3px solid #ff6b6b;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {
        display: none;
    }
    
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .stApp > header {
        display: none;
    }
    
    .stSelectbox label {
        color: #fff !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox > label {
        display: block !important;
        color: #fff !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Dark scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ff6b6b;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to fetch movie details from OMDb
@st.cache_data
def fetch_movie_details(movie_name, api_key="b9686597"):
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data if data.get("Response") == "True" else None
    except Exception as e:
        st.error(f"Error fetching movie details: {str(e)}")
        return None

# Function to recommend movies
@st.cache_data
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_movie_names = []
        recommended_movie_posters = []
        
        for i in distances[1:6]:
            name = movies.iloc[i[0]].title
            recommended_movie_names.append(name)
            
            details = fetch_movie_details(name)
            poster = details.get('Poster') if details and details.get('Poster') != 'N/A' else "https://via.placeholder.com/300x450/333333/ffffff?text=No+Image"
            recommended_movie_posters.append(poster)
        
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], []

# Load CSS
load_css()

# Load data with error handling
try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarty.pkl', 'rb'))
except FileNotFoundError:
    st.error("🚫 Data files not found! Please ensure 'movies.pkl' and 'similarty.pkl' are in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"🚫 Error loading data: {str(e)}")
    st.stop()

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; padding: 3rem 0 4rem 0; margin-bottom: 3rem;">
    <h1 class="main-title">🎬 CINEMAX</h1>
    <p class="subtitle">Discover Your Next Favorite Movie</p>
</div>
""", unsafe_allow_html=True)

# Search section
st.markdown('<div class="search-section">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h3 class="search-title">🔍 Select a Movie</h3>', unsafe_allow_html=True)
    
    # Method 1: Using selectbox with better visibility
    movie_list = movies['title'].dropna().tolist()
    
    # Initialize session state for selected movie if not exists
    if 'selected_movie_name' not in st.session_state:
        st.session_state.selected_movie_name = ""
    
    selected_movie = st.selectbox(
        "Choose from our movie database:",
        options=[""] + movie_list,  # Empty string as first option
        format_func=lambda x: "Type to search movies..." if x == "" else x,
        help="Type to search for movies",
        key="movie_search_box"
    )
    
    # Update session state when selection changes
    if selected_movie and selected_movie != "":
        st.session_state.selected_movie_name = selected_movie
    
    # Display the selected movie clearly
    if st.session_state.selected_movie_name:
        st.success(f"✅ Selected: **{st.session_state.selected_movie_name}**")
    
    recommend_clicked = st.button('🎯 GET RECOMMENDATIONS')

# Alternative Method 2: Using text_input with autocomplete-like behavior
# Uncomment this section if you prefer text input approach


st.markdown('</div>', unsafe_allow_html=True)

# Results section
if recommend_clicked and selected_movie:
    # Loading animation
    with st.spinner('🎭 Finding perfect matches for you...'):
        
        # Fetch main movie details
        main_movie_details = fetch_movie_details(selected_movie)
        
        if main_movie_details:
            st.markdown('<div class="movie-details">', unsafe_allow_html=True)
            
            st.markdown("<h3>🎬 SELECTED MOVIE</h3>", unsafe_allow_html=True)
            
            col_poster, col_info = st.columns([1, 2])
            
            with col_poster:
                poster_url = main_movie_details.get("Poster")
                if poster_url and poster_url != "N/A":
                    st.markdown(f'<img src="{poster_url}" class="movie-poster" width="300">', unsafe_allow_html=True)
                else:
                    st.markdown('<img src="https://via.placeholder.com/300x450/333333/ffffff?text=No+Image" class="movie-poster" width="300">', unsafe_allow_html=True)
            
            with col_info:
                st.markdown('<div class="movie-info">', unsafe_allow_html=True)
                
                # Movie details
                details = [
                    ("🎬 Title", main_movie_details.get('Title', 'N/A')),
                    ("📅 Year", main_movie_details.get('Year', 'N/A')),
                    ("⭐ IMDB Rating", main_movie_details.get('imdbRating', 'N/A')),
                    ("🎭 Genre", main_movie_details.get('Genre', 'N/A')),
                    ("🎬 Director", main_movie_details.get('Director', 'N/A')),
                    ("⏱️ Runtime", main_movie_details.get('Runtime', 'N/A')),
                    ("📝 Plot", main_movie_details.get('Plot', 'N/A')[:200] + "..." if main_movie_details.get('Plot', 'N/A') != 'N/A' and len(main_movie_details.get('Plot', 'N/A')) > 200 else main_movie_details.get('Plot', 'N/A'))
                ]
                
                for icon_label, value in details:
                    if value and value != 'N/A':
                        st.markdown(f'<div class="movie-stat"><strong>{icon_label}:</strong> {value}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Divider
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        
        # Recommendations
        st.markdown('<div class="recommendations">', unsafe_allow_html=True)
        st.markdown('<h2 class="recommendations-title">🎯 RECOMMENDED FOR YOU</h2>', unsafe_allow_html=True)
        
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
        if recommended_movie_names:
            cols = st.columns(5)
            
            for i in range(min(5, len(recommended_movie_names))):
                with cols[i]:
                    st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
                    
                    poster_url = recommended_movie_posters[i]
                    st.markdown(f'<img src="{poster_url}" class="recommendation-poster" alt="{recommended_movie_names[i]}">', unsafe_allow_html=True)
                    st.markdown(f'<div class="recommendation-title">{recommended_movie_names[i]}</div>', unsafe_allow_html=True)
                    
                    # Add movie index/number
                    st.markdown(f'<div style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">#{i+1} Recommendation</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("🤔 Sorry, we couldn't find recommendations for this movie. Please try another one!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🎭 CINEMAX • Powered by AI & Movie Intelligence • Made for Cinema Lovers</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)