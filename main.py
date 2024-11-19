import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Initialize session state for user management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# Load or create reservation data
def load_reservations():
    try:
        if os.path.exists('reservations.json'):
            with open('reservations.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading reservations: {e}")
    
    # Default reservation structure
    default_reservations = {
        'tables': {
            'Ichiban Table': {'seats': {str(i): None for i in range(1, 21)}}
        }
    }
    
    # Save default structure if file doesn't exist
    save_reservations(default_reservations)
    return default_reservations

def save_reservations(data):
    try:
        # Simply save to current directory
        with open('reservations.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving reservations: {e}")

# Login system
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        # In a real application, you would verify credentials against a database
        st.session_state.logged_in = True
        st.session_state.username = username
        st.experimental_rerun()

def add_custom_css():
    st.markdown("""
        <style>
        /* Modern container styling */
        .stApp {
            background-color: #1a1a2e;
            color: #ffffff;
        }
        
        /* Custom title styling */
        h1, h2, h3 {
            color: #4dd0e1;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* Hibachi table styling */
        .hibachi-container {
            background: linear-gradient(145deg, #1a1a2e, #1f1f3a);
            border-radius: 20px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .grill-center {
            background: linear-gradient(145deg, #2a2a45, #3a3a6a);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: #4dd0e1;
            font-weight: bold;
            border: 2px solid #4dd0e1;
            box-shadow: 0 0 15px rgba(77, 208, 225, 0.3);
        }
        
        /* Seat styling */
        .seat-box {
            background: linear-gradient(145deg, #1d1d35, #2a2a45);
            border: 2px solid #4dd0e1;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            margin: 5px;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .seat-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 15px rgba(77, 208, 225, 0.4);
        }
        
        .reserved {
            background: linear-gradient(145deg, #2a1f1f, #3a2a2a);
            border-color: #ff4444;
            box-shadow: 0 4px 12px rgba(255,68,68,0.2);
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(145deg, #4dd0e1, #00bcd4);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(77, 208, 225, 0.4);
        }
        
        /* Status indicator */
        .status-indicator {
            font-size: 0.8em;
            color: #4dd0e1;
            margin-top: 5px;
        }
        
        /* Seat number badge */
        .seat-number {
            position: relative;
            font-size: 1.2em;
            font-weight: bold;
            color: #4dd0e1;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_seat_layout(table_data):
    add_custom_css()
    
    st.markdown('<div class="hibachi-container">', unsafe_allow_html=True)
    
    # Top row (6 seats)
    top_row = st.columns(8)
    # Middle section
    left_side, center, right_side = st.columns([2, 4, 2])
    # Bottom row (6 seats)
    bottom_row = st.columns(8)
    
    def display_seat(seat_num, reserved_by):
        if reserved_by:
            st.markdown(f"""
                <div class="seat-box reserved">
                    <div class="seat-number">#{seat_num}</div>
                    <div class="status-indicator">Reserved</div>
                    <small>{reserved_by}</small>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="seat-box">
                    <div class="seat-number">#{seat_num}</div>
                    <div class="status-indicator">Available</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Reserve", key=f"seat-{seat_num}"):
                return True
        return False

    seats = table_data['seats']
    
    # Display top row (seats 1-8)
    for i, col in enumerate(top_row):
        with col:
            if display_seat(str(i + 1), seats[str(i + 1)]):
                return str(i + 1)

    # Display side seats
    for i in range(2):
        with left_side:
            if display_seat(str(i + 9), seats[str(i + 9)]):
                return str(i + 9)
    
    # Display grill center
    with center:
        st.markdown("""
            <div class="grill-center">
                <div style="font-size: 1.5em; margin-bottom: 10px;">🔥</div>
                Hibachi Grill
                <div style="font-size: 0.8em; margin-top: 10px;">Master Chef's Station</div>
            </div>
        """, unsafe_allow_html=True)
    
    for i in range(2):
        with right_side:
            if display_seat(str(i + 11), seats[str(i + 11)]):
                return str(i + 11)

    # Display bottom row (seats 13-20)
    for i, col in enumerate(bottom_row):
        seat_num = str(i + 13)
        with col:
            if display_seat(seat_num, seats[seat_num]):
                return seat_num

    st.markdown('</div>', unsafe_allow_html=True)
    return None

# Main app
def main():
    st.markdown("""
        <h1 style='text-align: center; color: #4dd0e1; margin-bottom: 2em;'>
            🍜 Ichiban Hibachi Experience
        </h1>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        login()
        st.warning("Please login to make a reservation")
        return
    
    reservations = load_reservations()
    st.markdown(f"""
        <h2 style='text-align: center; color: #4dd0e1; margin-bottom: 1em;'>
            Welcome, {st.session_state.username}! 
        </h2>
    """, unsafe_allow_html=True)
    
    # Display the table layout
    for table_name, table_data in reservations['tables'].items():
        st.markdown(f"""
            <h3 style='text-align: center; color: #4dd0e1; margin: 1em 0;'>
                {table_name}
            </h3>
        """, unsafe_allow_html=True)
        
        reserved_seat = create_seat_layout(table_data)
        
        if reserved_seat:
            reservations['tables'][table_name]['seats'][reserved_seat] = st.session_state.username
            save_reservations(reservations)
            st.experimental_rerun()
    
    # Logout button in sidebar
    with st.sidebar:
        st.markdown("<div style='padding: 1em;'>", unsafe_allow_html=True)
        if st.button("Logout", key="logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()