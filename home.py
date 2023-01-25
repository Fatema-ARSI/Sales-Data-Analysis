import streamlit as st
import base64


#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class home_page(HydraHeadApp):


    def run(self):
        #sidebar section
        # Main panel
        st.markdown("""# Alternative Investemnt Project""")

        st.markdown(""" To add text here about the project """)


        st.markdown(""" --- Note: This is app can be used for information purpose only. """)
        st.markdown(""" * Python libraries: `Yahoo Finance`, `Pandas`, `Streamlit`, `Plotly`,`Hydralit`,`Tensorflow`, `Linear Regression`, `Pyportfolioopt`,`VaderSentiment`  """)
