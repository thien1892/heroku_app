import streamlit as st
import cv2
from models import app_scan
from multiapp import MultiApp

st.write(
    """
    # Demo app with opencv
    """
)

app = MultiApp()

app.add_app('Scan documents', app_scan.app)

app.run()