#!/usr/bin/env python3
import streamlit as st
import streamlit.components.v1 as components

# interactive cljs
my_component = components.declare_component("my_component", path="frontend/public")
num_clicks = my_component(default=0)
st.markdown("You've clicked %s times!" % int(num_clicks))
