from htbuilder import div, big, h2, styles
from htbuilder.units import rem
import streamlit as st
import time


COLOR_RED = "#FF4B4B"
COLOR_BLUE = "#1C83E1"
COLOR_CYAN = "#00C0F2"
COLOR_ORANGE = "#FFA500"
COLOR_GREEN = "#00FF00"

def display_callout(title, color, icon, second_text):
    st.markdown(
        div(
            style=styles(
                background_color=color,
                padding=rem(1),
                display="flex",
                flex_direction="row",
                border_radius=rem(0.5),
                margin=(0, 0, rem(0.5), 0),
            )
        )(
            div(style=styles(font_size=rem(2), line_height=1))(icon),
            div(style=styles(padding=(rem(0.5), 0, rem(0.5), rem(1))))(title),
        ),
        unsafe_allow_html=True,
    )

def display_small_text(text):
    st.markdown(
        div(
            style=styles(
                font_size=rem(0.8),
                margin=(0, 0, rem(1), 0),
            )
        )(text),
        unsafe_allow_html=True,
    )

def display_dial(title, value, color):
    st.markdown(
        div(
            style=styles(
                text_align="center",
                color=color,
                padding=(rem(0.8), 0, rem(3), 0),
            )
        )(
            h2(style=styles(font_size=rem(0.8), font_weight=600, padding=0))(title),
            big(style=styles(font_size=rem(2), font_weight=800, line_height=1))(
                value
            ),
        ),
        unsafe_allow_html=True,
    )


def display_dial_v2(cell, title, value, color):
        cell.markdown(
        div(
            style=styles(
                text_align="left",
                color=color,
                padding=(rem(0.8), 0, rem(3), 0),
            )
        )(
            h2(style=styles(font_size=rem(1), font_weight=600, padding=0))(title),
            big(style=styles(font_size=rem(2), font_weight=700, line_height=1))(
                value
            ),
        ),
        unsafe_allow_html=True,
    )

def animation(target_value, title, color, string=False):
        current_value = target_value - 1000 if target_value > 1000 else 0
        empty = st.empty()
        while current_value < target_value:
            current_value += 1
            time.sleep(0.00001)
            if string:        
                display_dial_v2(empty, title, str(current_value) + '%', color)
            else:
                display_dial_v2(empty, title, current_value, color)
        if string:
            display_dial_v2(empty, title, str(target_value) + '%', color)
        else:
            display_dial_v2(empty, title, target_value, color)