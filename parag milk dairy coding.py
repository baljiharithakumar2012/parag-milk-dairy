import streamlit as st
import os

st.title("🧀 Parag Dairy App - Center Based Posting")

menu = st.sidebar.selectbox("Choose Login Role", ["Admin", "Employee", "Farmer"])

UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def get_center_filename(center, role):
    filename = f"{role.lower()}_{center.lower().replace(' ', '_')}.txt"
    return os.path.join(UPLOADS_DIR, filename)

def ai_quality_report(fat, snf):
    report = []
    if fat < 4:
        report.append("⚠️ Fat is low. Improve fat content.")
    if snf < 4:
        report.append("⚠️ SNF is low. Improve SNF.")
    if not report:
        report.append("✅ Milk quality is good.")
    return "\n".join(report)

def show_upload_form(role, center="all"):
    st.subheader(f"{role} Upload Section for Center: {center}")
    message = st.text_area("Enter a message or update")
    uploaded_file = st.file_uploader("Upload a file (optional)", type=['pdf', 'txt', 'csv', 'png', 'jpg', 'jpeg'])

    fat = st.number_input("Enter Fat value", min_value=0.0, step=0.1)
    snf = st.number_input("Enter SNF value", min_value=0.0, step=0.1)

    if st.button("Post"):
        file_path = get_center_filename(center, role)
        with open(file_path, "a") as f:
            if message:
                f.write(f"Message: {message}\n")
            f.write(f"Fat: {fat}, SNF: {snf}\n")
            f.write("------\n")
        if uploaded_file:
            save_path = os.path.join(UPLOADS_DIR, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File '{uploaded_file.name}' uploaded.")

        st.info(ai_quality_report(fat, snf))

def show_farmers_view(center):
    st.subheader(f"📥 Farmer View for Center: {center}")
    # Read posts from employees and admins for this center
    employee_file = get_center_filename(center, "employee")
    admin_file = get_center_filename("all", "admin")

    if os.path.exists(admin_file):
        st.markdown("**Admin Messages:**")
        with open(admin_file, "r") as f:
            st.text(f.read())

    if os.path.exists(employee_file):
        st.markdown("**Employee Messages:**")
        with open(employee_file, "r") as f:
            st.text(f.read())

    # Show uploaded files
    files = [f for f in os.listdir(UPLOADS_DIR) if f.endswith(('.pdf', '.txt', '.csv', '.png', '.jpg', '.jpeg'))]
    if files:
        st.markdown("**Uploaded Files:**")
        for file in files:
            file_path = os.path.join(UPLOADS_DIR, file)
            st.markdown(f"- [{file}](./{file_path})")
    else:
        st.write("No files uploaded yet.")

# ---- Login Logic ----
def login(role, user_id, expected_id, password_input):
    return user_id == expected_id and password_input == "parag.in"

centers = ["Palamaner", "Madanapalle", "Kuppam", "Punganur", "Mulakalacheruvu"]

if menu == "Admin":
    st.subheader("Admin Login")
    user = st.text_input("Admin ID")
    password = st.text_input("Password", type="password")
    if st.button("Login as Admin"):
        if login("admin", user, "admin.parag.in", password):
            st.success("Welcome Admin!")
            show_upload_form("admin", center="all")
        else:
            st.error("Invalid admin credentials.")

elif menu == "Employee":
    st.subheader("Employee Login")
    user = st.text_input("Employee ID")
    password = st.text_input("Password", type="password")
    center = st.selectbox("Select Your Collection Center", centers)
    if st.button("Login as Employee"):
        if login("employee", user, "parag.workers.in", password):
            st.success(f"Welcome Employee from {center}")
            show_upload_form("employee", center=center)
        else:
            st.error("Invalid employee credentials.")

elif menu == "Farmer":
    st.subheader("Farmer Login")
    user = st.text_input("Farmer ID")
    password = st.text_input("Password", type="password")
    center = st.selectbox("Select Your Collection Center", centers)
    if st.button("Login as Farmer"):
        if login("farmer", user, "paragmilk.in", password):
            st.success(f"Welcome Farmer from {center}")
            show_farmers_view(center=center)
        else:
            st.error("Invalid farmer credentials.")
