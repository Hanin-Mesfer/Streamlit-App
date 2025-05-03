import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# File uploader to upload a CSV file
file = st.file_uploader("Upload CSV file", type=["csv"])

if file is not None:
    df = load_data(file)

    st.markdown("### 👁️Uncover Your Data’s Story")

    # Slider to choose number of rows to display
    n_rows = st.slider('Choose number of rows to display',
                       min_value=5, max_value=len(df), step=1)

    # Multi-select to choose columns to display
    columns_to_show = st.multiselect("Select columns to show",
                                     df.columns.to_list(), default=df.columns.to_list())

    # Identify numerical columns
    numerical_columns = df.select_dtypes(include=np.number).columns.to_list()

    # Display selected data preview
    st.write(df[columns_to_show].head(n_rows))

    # Warning message if no numerical columns found
    if not numerical_columns:
        st.warning("⚠️ Oops! It looks like there are no numerical columns available for plotting. Please check your dataset for numeric values to create engaging visualizations.")
    else:
        # Tabs to switch between different plots
        tab1, tab2 ,tab3, tab4 = st.tabs(["📊 Scatter plot", "📈 Histogram", "📊 Pie Chart", "📉 KDE Chart"])

        # Scatter Plot Tab
        with tab1:
            st.markdown("### Discover How Your Data Features Relate")
            st.markdown(
                "*Want to see if two numbers go up or down together? Try a scatter plot! Just choose what you want on the X and Y sides, and add some color to make patterns easier to see.*"
            )

            col1, col2, col3 = st.columns(3)

            default_x = numerical_columns[0] if numerical_columns else None
            default_y = numerical_columns[1] if len(numerical_columns) > 1 else default_x

            # Column selection for scatter plot axes
            with col1:
                x_column = st.selectbox('Select column for X-axis:', numerical_columns, index=0)
            with col2:
                y_column = st.selectbox('Select column for Y-axis:', numerical_columns, index=1 if len(numerical_columns) > 1 else 0)
            with col3:
                color = st.selectbox('Select column for color grouping:', df.columns)

            # Create and display scatter plot
            fig_scatter = px.scatter(df, x=x_column, y=y_column, color=color)
            st.plotly_chart(fig_scatter)

        # Histogram Tab
        with tab2:
            st.markdown("### 📈 Discover the Distribution!")

            # Select feature for histogram
            histogram_feature = st.selectbox('Select feature for histogram:', df.columns)

            # Create and display histogram
            fig_hist = px.histogram(df, x=histogram_feature, nbins=30, color_discrete_sequence=["#636EFA"])
            st.plotly_chart(fig_hist)

        # Pie Chart Tab
        with tab3:
            st.markdown("###  Categorical Data Overview")
            st.markdown("*A pie chart provides a simple and intuitive way to visualize the proportion of each category within a selected column. It helps in understanding how the data is distributed across different groups.*")

            # Select categorical feature for pie chart
            pie_feature = st.selectbox('Select feature for pie chart:', df.select_dtypes(include='object').columns)

            # Create and display pie chart
            fig_pie = px.pie(df, names=pie_feature, title=f"Pie Chart for {pie_feature}")
            st.plotly_chart(fig_pie)

        # KDE Chart Tab
        with tab4:
            st.markdown("### 📉 Visualizing Data Distribution – KDE Plot")
            st.markdown("The Kernel Density Estimate (KDE) plot is a useful tool to visualize the probability distribution of a numerical variable.Unlike histograms, KDE plots provide a smooth curve that represents the density of data points over a continuous range")

            kde_feature = st.selectbox('Select feature for KDE plot:', numerical_columns, key="kde_selectbox")
            # Create KDE plot using Seaborn
            plt.figure(figsize=(10, 6))
            sns.kdeplot(df[kde_feature], shade=True, color="darkgreen")  # shade=True fills the area under the curve
            plt.title(f"Filled KDE Plot for {kde_feature}", fontsize=16)
            plt.xlabel(kde_feature, fontsize=12)
            plt.ylabel("Density", fontsize=12)  # "Density" can be changed to a more specific label based on context

            # Display plot in Streamlit
            st.pyplot(plt)
