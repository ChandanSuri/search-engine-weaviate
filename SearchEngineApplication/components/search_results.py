import streamlit as st
from streamlit_modal import Modal
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def render_product_card(product: Dict) -> None:
    """Render an individual product card with modal details"""
    stars = "⭐" * int(product["rating"]) + "☆" * (5 - int(product["rating"]))

    st.markdown(
        f"""
        <div class="card">
            <div>
                <div class="card-title">{product['title']}</div>
                <div class="card-brand">{product['brand']}</div>
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
            st.markdown(f"**Brand:** {product['brand']}")
            st.markdown(f"**Color:** {product['color']}")
            st.write(product['description'])

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