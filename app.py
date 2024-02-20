import streamlit as st 
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import streamlit_shadcn_ui as ui


st.set_page_config(page_title="GovSkills", page_icon=None, layout="wide")

#load csv to github 
df = pd.read_csv("https://raw.githubusercontent.com/mtworth/govskillsapp/main/fake_govskills.csv")

# Initialize the dialog to be shown by default when the app loads
if 'show_dialog' not in st.session_state:
    st.session_state.show_dialog = True

# Define a function to toggle the dialog visibility
def toggle_dialog():
    st.session_state.show_dialog = not st.session_state.show_dialog

# Check if the dialog should be shown
if st.session_state.show_dialog:
    # Assuming the dialog component can be controlled by passing a boolean to `show`
    # Replace `ui.alert_dialog` with the correct function call if needed
    confirm = ui.alert_dialog(show=True, title="⚒️ GovSkills Alpha ⚒️", description="Welcome to the alpha dashboard for GovSkills, an application tool that provides insight into federal hiring. Please be aware that this build may contain bugs and is undergoing changes. Please reach out to provide feedback.", cancel_label= "Contact GovSkills", confirm_label="Show me the data!", key="alert_dialog_1")

    
    # If the user clicks "OK" or "Cancel", hide the dialog
    if confirm:
        toggle_dialog()


##enable filtering 
#clean up text
with st.sidebar:
    st.title("GovSkills")
    st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")

    st.text_input("Enter keywords for job description")
    agencies = df['Federal Agency'].drop_duplicates()
    states = df['State'].drop_duplicates()
    agency_choice = st.sidebar.selectbox('Filter agency:', agencies)
    state_choice = st.sidebar.selectbox('Filter state:', states)
    start_date = st.date_input("What is the earliest posting date you'd like to see?")
    end_date = st.date_input("What is the latest posting date you'd like to see?")

st.markdown("Query Results from "  + str(start_date) + " to " + str(end_date))


unique_agencies = df['Federal Agency'].nunique()
total_jobs = df.shape[0]


df['Posting Date'] = pd.to_datetime(df['Posting Date'])
# Assuming df['Posting Date'] is already converted to datetime
df['Posting Month-Year'] = df['Posting Date'].dt.to_period('M')

# Set the day to the first day of the month
df['Posting Month-Year'] = df['Posting Month-Year'].dt.strftime('%Y-%m-01')

# Count the occurrences of each month-year combination
monthly_yearly_counts = df['Posting Month-Year'].value_counts().reset_index()
monthly_yearly_counts.columns = ['Posting Month-Year', 'Count']

# If you want the 'Posting Month-Year' column as a datetime type, you can convert it back
monthly_yearly_counts['Posting Month-Year'] = pd.to_datetime(monthly_yearly_counts['Posting Month-Year'])


col1, col2 = st.columns([1, 2])


#fix formatting
with col1:
    with st.container(border=True, height = 150):
            image1, text1 = st.columns(2)

            with image1:
                st.image("https://static.vecteezy.com/system/resources/previews/002/077/041/original/people-icon-in-blue-circle-free-vector.jpg",width=100)
            with text1:
                st.title(total_jobs)
                st.caption('Jobs Posted')

    with st.container(border=True, height = 150):
            image2, text2 = st.columns(2)

            with image2:
                st.image("https://static.vecteezy.com/system/resources/previews/002/077/041/original/people-icon-in-blue-circle-free-vector.jpg",width=100)
            with text2:
                st.title("23")
                st.caption('Agencies Hiring')

    with st.container(border=True, height = 150):
            image3, text3 = st.columns(2)

            with image3:
                st.image("https://static.vecteezy.com/system/resources/previews/002/077/041/original/people-icon-in-blue-circle-free-vector.jpg",width=100)
            with text3:
                st.title("$121.1k")
                st.caption('Median Salary')


with col2: 
    with st.container(border=True):
        st.markdown("**Count of Jobs by Posting Date**")

        big_chart = alt.Chart(monthly_yearly_counts).mark_area(
                line={'color':'#4287f5'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='white', offset=0),
                        alt.GradientStop(color='#4287f5', offset=1)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0
                )
            ).encode(
                alt.X('Posting Month-Year:T',axis=alt.Axis(title="Posted Date", grid=False)),
                alt.Y('Count:Q',axis=alt.Axis(title="Job Count", grid=False))
            )
        st.altair_chart(big_chart, use_container_width=True)

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])


# Group by 'Federal Agency' and count the occurrences
agency_counts = df['Federal Agency'].value_counts().reset_index()
agency_counts.columns = ['Agency', 'Count']
agency_counts = agency_counts.sort_values('Count', ascending=False)

col4, col5, col6 = st.columns(3)

##convert to agency count
with col4:
    with st.container(border=True,height=300):
        st.markdown("**Jobs by Agency**")

        # Create an Altair bar chart
        chart = alt.Chart(agency_counts).mark_bar().encode(
            x='Count:Q',
            y=alt.Y('Agency:N', sort='-x')
        )

        # Update chart configuration
        chart = chart.properties(
            height=600
        )

        # Display the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)




##convert to occ series count
with col5:
    with st.container(border=True, height=300):
        st.markdown("**Jobs by Agency**")
        st.altair_chart(chart, use_container_width=True)

        #st.bar_chart(agency_counts,height=300,x="Count",y="Agency")


##convert to position title count
with col6:
    with st.container(border=True, height=300):
        st.markdown("**Jobs by Agency**")
        st.altair_chart(chart, use_container_width=True)

#        st.bar_chart(chart_data, height=600)


## add pagination, URL redirect. Remove the index. 
with st.container(border=True):
    st.markdown("**Most Recent Open Jobs**")

    selected_columns = ['Posting Date', 'Federal Agency', 'Position Title', 'Hiring Path','OCC Series Code', 'Grade','Salary']
    df_selected = df[selected_columns]
    df_selected['USAJOBS Link'] = "www.usajobs.gov"
    st.dataframe(df_selected.head(10),hide_index=True,column_config={
        "Salary": st.column_config.ProgressColumn(
            "Salary Estimate",
            help="Estimated Salary Derived from Grade",
            format="$%f",
            min_value=0,
            max_value=200000,
        )})


