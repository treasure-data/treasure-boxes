"""
Style management for CJO Profile Viewer

This module provides utilities for loading CSS styles for the Streamlit application.
"""

import streamlit as st
import os
from pathlib import Path


def load_css_file(css_file: str) -> str:
    """
    Load CSS content from a file.

    Args:
        css_file: Name of the CSS file (without path)

    Returns:
        CSS content as string
    """
    styles_dir = Path(__file__).parent
    css_path = styles_dir / css_file

    try:
        with open(css_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"CSS file not found: {css_file}")
        return ""


def inject_css(css_content: str) -> None:
    """
    Inject CSS into the Streamlit app.

    Args:
        css_content: CSS content to inject
    """
    if css_content:
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def load_all_styles() -> None:
    """Load all application styles."""
    # Load layout styles
    layout_css = load_css_file("layout.css")
    inject_css(layout_css)

    # Load button styles
    button_css = load_css_file("buttons.css")
    inject_css(button_css)


def load_flowchart_styles() -> str:
    """
    Load flowchart-specific styles for HTML generation.

    Returns:
        Flowchart CSS wrapped in style tags
    """
    flowchart_css = load_css_file("flowchart.css")
    modal_css = load_css_file("modal.css")

    if flowchart_css or modal_css:
        return f"<style>\n{flowchart_css}\n{modal_css}\n</style>"
    return ""


# Style categories for selective loading
STYLE_CATEGORIES = {
    "layout": "layout.css",
    "buttons": "buttons.css",
    "flowchart": "flowchart.css",
    "modal": "modal.css"
}


def load_styles(*categories: str) -> None:
    """
    Load specific style categories.

    Args:
        *categories: Style categories to load (layout, buttons, flowchart, modal)
    """
    for category in categories:
        if category in STYLE_CATEGORIES:
            css_content = load_css_file(STYLE_CATEGORIES[category])
            inject_css(css_content)
        else:
            st.warning(f"Unknown style category: {category}")