import streamlit as st
from streamlit_modal import Modal
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def render_product_card(product: Dict) -> None:
    """Render an individual product card with modal details"""
    rating = product.get("rating", 0)
    stars = "⭐" * int(rating) + "☆" * (5 - int(rating)) if rating > 0 else "No rating"

    color_display = product.get('color', 'N/A') if product.get('color') else 'N/A'
    price_display = product.get('price', 'Price not available')

    st.markdown(
        f"""
        <div class="card">
            <div>
                <div class="card-title">{product['title']}</div>
                <div class="card-brand">{product['brand']}</div>
                <div style="color: #94A3B8; margin-top: 0.5rem;">
                    Color: {color_display} | {price_display}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    modal = Modal(product['title'], key=f"modal_{product['id']}", padding=20, max_width=640)
    if st.button("View Details", key=f"details_{product['id']}", use_container_width=True):
        logger.info(f"Opening modal for product: {product['title']}")
        modal.open()

    if modal.is_open():
        with modal.container():
            st.markdown(f"### {product['title']}")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Brand:** {product['brand']}")
                st.markdown(f"**Color:** {color_display}")
                st.markdown(f"**Price:** {price_display}")
                if rating > 0:
                    st.markdown(f"**Rating:** {stars} ({rating}/5)")

            with col2:
                st.markdown(f"**Product ID:** {product['id']}")
                if product.get('reviews', 0) > 0:
                    st.markdown(f"**Reviews:** {product['reviews']}")

            if product.get('description'):
                st.markdown("**Description:**")
                # Remove HTML tags from description for better display
                clean_description = product['description'].replace('<br>', '\n').replace('<BR>', '\n')
                st.markdown(clean_description)

            if product.get('bullet_points'):
                st.markdown("**Key Features:**")
                st.markdown(product['bullet_points'])

def render_search_results(products: List[Dict]) -> None:
    """Render the complete search results section"""
    logger.info(f"Rendering search results with {len(products)} products")

    st.header("Search Results")

    results_container = st.container(height=800)
    with results_container:
        if products:
            grid_cols = st.columns(2)
            for i, product in enumerate(products):
                with grid_cols[i % 2]:
                    render_product_card(product)
        else:
            logger.warning("No products to display")
            st.info("No products found.")