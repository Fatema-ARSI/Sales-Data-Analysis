from hydralit import HydraApp
import streamlit as st
from home import home_page
from part1 import performance
from part2 import index
from part3 import correlated_etf
from part4 import noncorrelated_etfs



if __name__ == '__main__':
    #this is the host application, we add children to it and that's it!
    app = HydraApp(title='Stock Prediction with News-Events Analysis',favicon="",nav_horizontal=True,hide_streamlit_markers=True)

   # The Home app, this is the default redirect if no target app is specified.
    app.add_app("Home", icon="", app=home_page(),is_home=True)

    app.add_app("Tanya's part", icon="", app=performance())
    app.add_app("Emma's part", icon="", app=index())
    app.add_app("Fatema's part1", icon="", app=correlated_etf())
    app.add_app("Fatema's part2", icon="", app=noncorrelated_etfs())




    #run the whole lot
    app.run()


st.info('Coded by 👩🏻‍💻[Fatema ARSIWALA](https://www.linkedin.com/in/fatemaarsi/)')
st.markdown("""
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)
