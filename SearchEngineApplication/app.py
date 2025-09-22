import streamlit as st
import logging
from utils import check_backend_health, get_available_brands, get_available_colors, search_products
from components.search_interface import render_search_interface
from components.chat import render_chat_interface
from components.search_results import render_search_results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Semantic Search Engine", layout="wide")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
    }

    h1 { color: #FAFAFA; }
    h2, h3 { color: #E0E0E0; padding-bottom: 1rem;}

    [data-testid="stChatMessageContent"] {
        background-color: #1E293B;
        border-radius: 15px;
        padding: 12px;
    }
    [data-testid="stChatMessageContent"] p {
        color: #FAFAFA;
    }

    .card {
        background-color: #181E29;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
        transition: box-shadow 0.3s ease, border-color 0.3s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card:hover {
        box-shadow: 0 4px 20px rgba(45, 212, 191, 0.2);
        border-color: #14B8A6;
    }
    .card-title {
        color: #14B8A6;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .card-brand {
        color: #FFFFFF;
        font-weight: bold;
    }

    .stButton > button, .stFormSubmitButton > button {
        border-radius: 20px;
        background-color: #14B8A6;
        color: #0E1117;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background-color: #0F766E;
        color: white;
    }

    div[data-testid="stModal"] {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 9999;
    }
    div[data-testid="stModal"] > div:first-child {
        position: relative !important;
        width: 90%;
        max-width: 640px;
        transform: none !important;
        border-radius: 15px;
        background-color: #0E1117;
        border: 1px solid #334155;
    }

    /* Fix sidebar icon rendering */
    [data-testid="stSidebarNav"] button,
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebar"] button {
        font-family: 'Inter', 'Source Sans Pro', sans-serif !important;
    }

    /* Ensure proper icon font loading */
    [data-testid="stSidebarNav"] svg,
    [data-testid="collapsedControl"] svg {
        display: inline-block !important;
        width: 16px !important;
        height: 16px !important;
    }

    /* Fix sidebar expand/collapse button */
    [data-testid="baseButton-header"] {
        background-color: transparent !important;
        color: #FAFAFA !important;
    }

    /* Ensure sidebar control icons render correctly */
    button[kind="headerNoPadding"] {
        color: #FAFAFA !important;
        font-size: 16px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if "searched" not in st.session_state:
    st.session_state.searched = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "products" not in st.session_state:
    st.session_state.products = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "backend_connected" not in st.session_state:
    st.session_state.backend_connected = check_backend_health()
if "brands_cache" not in st.session_state:
    st.session_state.brands_cache = None
if "colors_cache" not in st.session_state:
    st.session_state.colors_cache = None
if "cache_loaded" not in st.session_state:
    st.session_state.cache_loaded = False
if "active_brand_filter" not in st.session_state:
    st.session_state.active_brand_filter = None
if "active_color_filter" not in st.session_state:
    st.session_state.active_color_filter = None

logger.info(f"App started - Backend connected: {st.session_state.backend_connected}")

if not st.session_state.backend_connected:
    st.warning("⚠️ Backend API is not running. Please start the backend server first.")
    st.code("cd backend && python run_server.py")
    st.info("💡 Make sure to set your OPENAI_API_KEY in the backend/.env file")

if not st.session_state.searched:
    render_search_interface()
else:
    logger.info(f"Rendering search results view (session: {st.session_state.session_id})")

    # Add search filters in sidebar
    with st.sidebar:
        st.markdown("### 🔍 Search Filters")

        if st.button("🔄 New Search", use_container_width=True):
            logger.info("New search button clicked")
            st.session_state.searched = False
            st.session_state.messages = []
            st.session_state.products = []
            st.session_state.session_id = None
            # Reset filters when starting new search
            st.session_state.active_brand_filter = None
            st.session_state.active_color_filter = None
            st.rerun()

        st.markdown("---")
        st.markdown("#### Filter Products")

        # Get original search query from session state
        original_query = ""
        if st.session_state.messages:
            original_query = st.session_state.messages[0]["content"]

        # Show active filters
        active_filters = []
        if st.session_state.active_brand_filter:
            active_filters.append(f"🏷️ Brand: {st.session_state.active_brand_filter}")
        if st.session_state.active_color_filter:
            active_filters.append(f"🎨 Color: {st.session_state.active_color_filter}")

        if active_filters:
            st.markdown("**Active Filters:**")
            for filter_text in active_filters:
                st.markdown(f"- {filter_text}")

            if st.button("🗑️ Clear Filters", use_container_width=True):
                st.session_state.active_brand_filter = None
                st.session_state.active_color_filter = None
                # Perform search with original query and no filters
                if original_query:
                    try:
                        with st.spinner("🔍 Searching without filters..."):
                            unfiltered_results = search_products(original_query)

                        if unfiltered_results and unfiltered_results.get("products"):
                            st.session_state.products = unfiltered_results["products"]
                            st.success(f"Filters cleared - showing all {len(unfiltered_results['products'])} results")
                            st.rerun()
                    except Exception as e:
                        logger.error(f"Error clearing filters: {str(e)}")
                        st.error("Error clearing filters")

        # Continue with existing code

        # Load brands/colors cache if not already loaded
        if not st.session_state.cache_loaded and st.session_state.backend_connected:
            with st.spinner("Loading filters..."):
                try:
                    st.session_state.brands_cache = get_available_brands() or []
                    st.session_state.colors_cache = get_available_colors() or []
                    st.session_state.cache_loaded = True
                except Exception as e:
                    logger.error(f"Failed to load cache: {str(e)}")
                    st.session_state.brands_cache = []
                    st.session_state.colors_cache = []
                    st.session_state.cache_loaded = True  # Prevent retry loops

        # Brand filter
        brands = st.session_state.brands_cache or []
        brand_options = ["All Brands"] + brands
        selected_brand = st.selectbox("Brand:", brand_options, key="brand_filter")

        # Color filter
        colors = st.session_state.colors_cache or []
        color_options = ["All Colors"] + colors
        selected_color = st.selectbox("Color:", color_options, key="color_filter")

        # Save filters button
        if st.button("💾 Save Filter Settings", use_container_width=True):
            brand_filter = None if selected_brand == "All Brands" else selected_brand
            color_filter = None if selected_color == "All Colors" else selected_color

            # Store filters in session state for future searches
            st.session_state.active_brand_filter = brand_filter
            st.session_state.active_color_filter = color_filter

            filter_description = []
            if brand_filter:
                filter_description.append(f"Brand: {brand_filter}")
            if color_filter:
                filter_description.append(f"Color: {color_filter}")

            if filter_description:
                st.success(f"✅ Filters saved: {', '.join(filter_description)}")
                st.info("💡 These filters will be applied to your next search query!")
            else:
                st.success("✅ All filters cleared!")

            logger.info(f"Filter settings saved - Brand: {brand_filter}, Color: {color_filter}")
            st.rerun()

    chat_col, results_col = st.columns([1, 3])

    with chat_col:
        render_chat_interface(st.session_state.session_id)

    with results_col:
        render_search_results(st.session_state.products)