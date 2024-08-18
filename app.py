import streamlit as st
import pandas as pd
import ydata_profiling
import base64

@st.cache_data
def generate_report(df, minimal, dark_mode):
    try:
        profile = ydata_profiling.ProfileReport(df, minimal=minimal, dark_mode=dark_mode)
        profile_html = profile.to_html()
        return profile_html
    except Exception as ex:
        st.error(f"Error generating report: {str(ex)}")
        return None

def display_custom_css():
    st.markdown(
        """
        <style>
        .header { padding: 10px; text-align: center; font-size: 2em; color: #007bff; font-family: 'Roboto', sans-serif; }
        .description { text-align: center; font-size: 1.2em; margin: 10px; font-family: 'Roboto', sans-serif; }
        .btn-primary { background-color: #007bff; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 10px 2px; cursor: pointer; border-radius: 5px; }
        .btn-primary:hover { background-color: #0056b3; }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_ui():
    st.set_page_config(page_title="Data Profiling App", layout="wide")
    display_custom_css()
    
    st.markdown('<div class="header">📊 Data Profiling App</div>', unsafe_allow_html=True)
    st.markdown('<div class="description">Upload your CSV file to generate and view a data profiling report directly on this page.</div>', unsafe_allow_html=True)

    st.sidebar.header("Customization Options")
    minimal = st.sidebar.checkbox("Minimal Report", value=True)
    dark_mode = st.sidebar.checkbox("Dark Mode", value=True)
    
    return minimal, dark_mode

def main():
    minimal, dark_mode = display_ui()
    
    uploaded_file = st.file_uploader("", type="csv", key="uploader")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if df is not None and not df.empty:
                st.success("✅ CSV file loaded successfully.")

                # Button to process and view the report
                if st.button("🔍 Process and View Report"):
                    # Generate the report
                    report_html = generate_report(df, minimal, dark_mode)
                    
                    if report_html:
                        st.success("📊 Report is ready!")
                        st.components.v1.html(report_html, height=800, scrolling=True)
                        
                        # Add download button with HTML content directly
                        if st.download_button(
                            label="📥 Download the report",
                            data=report_html,  # Directly use HTML content
                            file_name="data_profile.html",
                            mime="text/html",
                            key="download_button"
                        ):
                            st.success("📥 Report is being downloaded!")
                    else:
                        st.error("❌ Error generating the report.")
            else:
                st.error("⚠️ Loaded file is empty or invalid.")
        except Exception as ex:
            st.error(f"❌ Error loading CSV file: {str(ex)}")

if __name__ == "__main__":
    main()
