import streamlit as st
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256

client = MongoClient('mongodb://localhost:27017')
mydatabase = client['User']
mycollection = mydatabase['user']

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)

def user_registration(username, name, password):
    hashed_password = hash_password(password)
    user_data = {
        "username": username,
        "name": name,
        "password": hashed_password
    }
    mycollection.insert_one(user_data)
    st.success("Registration successful")

def user_login(username, password):
    user = mycollection.find_one({"username": username})
    if user and verify_password(password, user['password']):
        st.success("Login successful")
        return user
    else:
        st.error("Invalid username or password")
        return None

def dashboard(user):
    
    st.title("Dashboard")
    st.write(f"Successfully Logged In, {user}!")
    st.image("Login.jpg")  

def main():
    
    st.title("User Authentication")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if username and password:
                user = user_login(username, password)
                dashboard(user['name'])

    elif choice == "Register":
        st.header("Register")
        new_username = st.text_input("Enter a username")
        new_name = st.text_input("Enter Your Name")
        new_password = st.text_input("Enter a password", type='password')
        if st.button("Register"):
            if new_username and new_password:
                user_registration(new_username, new_name, new_password)
    
if __name__ == '__main__':
    main()
