# powerbi.py

import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as stc
import streamlit as st
import concurrent.futures

class Pwbi:
    def __init__(self):
        self.items = None

    def dashboard(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_items_df = executor.submit(pd.DataFrame, self.items)
            items_df = future_items_df.result()

            future_pyg_html = executor.submit(pyg.walk(items_df).to_html)
            pyg_html = future_pyg_html.result()

        if isinstance(pyg_html, str):
            custom_style = """
            <style>
            body, html {
                background-color: #1a1a1a !important; /* or use the specific color code for zinc-900 */
                color: #ffffff !important;
            }
            /* Add additional global styles for table, tr, td, th, etc., if necessary */
            </style>
            """

            head_index = pyg_html.find('</head>')
            if head_index != -1:
                pyg_html = pyg_html[:head_index] + custom_style + pyg_html[head_index:]
            else:
                pyg_html = custom_style + pyg_html

            stc.html(pyg_html, scrolling=True, height=970)
        else:
            print("Error: pyg.walk did not return a string.")