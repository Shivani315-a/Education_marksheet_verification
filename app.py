import streamlit as st
from verification import verify_marksheet

st.set_page_config(page_title="Marksheet Verification", layout="centered")

st.title("🎓 Marksheet Verification System")

name = st.text_input("Enter First Name")
surname = st.text_input("Enter Surname")

education_level = st.selectbox(
    "Select Education Level",
    ["10th", "12th", "diploma", "graduation", "postgraduation"]
)

uploaded_file = st.file_uploader("Upload Marksheet PDF", type=["pdf"])

if st.button("Verify"):

    if not uploaded_file:
        st.error("Please upload a PDF file.")

    elif not name or not surname:
        st.error("Please enter name and surname.")

    else:
        file_bytes = uploaded_file.read()

        result = verify_marksheet(
            file_bytes,
            name,
            surname,
            education_level
        )

        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("📄 Verification Details")

            st.write("Name Match:", result["name_match"],
                     f"(Score: {result['name_score']})")

            st.write("Surname Match:", result["surname_match"],
                     f"(Score: {result['surname_score']})")

            st.write("Education Match:", result["education_match"])
            st.write("Matched Keyword:", result["matched_keyword"])
            st.write("Result (Pass/Fail):", result["result"])

            if result["verified"]:
                st.success("Document Verified Successfully")
            else:
                st.error("Verification Failed")
