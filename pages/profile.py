import streamlit as st
from postgre import connect 
import os
import sys
sys.path.append(os.path.abspath("./../postgre"))

def show_user_profile(user_id):

    query = f"""
    SELECT first_name, last_name, phone_number, country, city, birth_date, issue_date, expiration_date
    FROM user_personal_info
    WHERE id = '{user_id}';
    """
    user_info = connect.fetch_all(query) 
    if user_info:
        user_info = user_info[0]
        st.write(f"**First Name:** {user_info[0]}")
        st.write(f"**Last Name:** {user_info[1]}")
        st.write(f"**Phone Number:** {user_info[2]}")
        st.write(f"**Country:** {user_info[3]}")
        st.write(f"**City:** {user_info[4]}")
        st.write(f"**Birth Date:** {user_info[5]}")
        st.write(f"**Passport Issue Date:** {user_info[6]}")
        st.write(f"**Passport Expiration Date:** {user_info[7]}")
    else:
        st.error("User not found!")


def main():

    
    if 'user_id' in st.session_state:
        print(st.session_state['user_id'])
        show_user_profile(st.session_state["user_id"])
    else:
        print('no')


# Запуск основной функции приложения
if __name__ == "__main__":
    main()
