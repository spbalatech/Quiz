import streamlit as st
import json
import os
import random
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from config import EMAIL_CONFIG

# Load data
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_resized_image(image_path, max_height=400):
    try:
        image = Image.open(image_path)
        # Calculate new width to maintain aspect ratio
        ratio = max_height / image.height
        new_width = int(image.width * ratio)
        # Resize image
        resized_image = image.resize((new_width, max_height))
        return resized_image
    except Exception as e:
        return None

def send_registration_email(name, mobile):
    try:
        msg = MIMEText(f"""
        New Quiz Registration:
        
        Name: {name}
        Mobile: {mobile}
        Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """)
        
        msg['Subject'] = 'New Samsung Quiz Registration'
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['receiver_email']
        
        with smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as smtp_server:
            smtp_server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['key'])
            smtp_server.sendmail(
                EMAIL_CONFIG['sender_email'],
                EMAIL_CONFIG['receiver_email'],
                msg.as_string()
            )
        return True
    except Exception as e:
        error_msg = str(e)
        if "BadCredentials" in error_msg:
            st.error("""Email configuration error. To fix this:
            1. Go to your Google Account settings
            2. Enable 2-Step Verification if not already enabled
            3. Go to Security > App passwords
            4. Generate a new app password for this application
            5. Update the key in config.py with the generated password""")
        else:
            st.error(f"Error sending email: {error_msg}")
        return False

def show_registration():
    st.title("Welcome to Samsung Smart Cafe Thanjavur Quiz")
    st.write("Please enter your details to start the quiz")
    
    name = st.text_input("Enter your name:", key="name_input")
    mobile = st.text_input("Enter your mobile number:", key="mobile_input")
    
    if st.button("Start Quiz"):
        if not name or not mobile:
            st.error("Please enter both name and mobile number")
            return False
        if not mobile.isdigit() or len(mobile) != 10:
            st.error("Please enter a valid 10-digit mobile number")
            return False
        
        # Send registration email
        if send_registration_email(name, mobile):
            st.success("Registration successful!")
            st.session_state.user_name = name
            st.session_state.user_mobile = mobile
            st.session_state.is_registered = True
            
            # Select random products when registration is successful
            products = load_json('data/products.json')['products']
            st.session_state.quiz_products = random.sample(products, 2)
            return True
        return False
    
    return False

def show_quiz():
    st.title("Samsung Smart Cafe Thanjavur Quiz")
    st.write(f"Welcome {st.session_state.user_name}!")
    st.write("Guess the price of these amazing products!")

    current_product = st.session_state.quiz_products[st.session_state.current_index]
    
    # Create columns with custom widths
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Product Details:")
        # Create a container for scrollable product details
        with st.container():
            st.write(f"Name: {current_product['name']}")
            st.write(f"Model: {current_product['model']}")
            st.write(f"Type: {current_product['type']}")
            st.write(f"Category: {current_product['category'].replace('_', ' ').title()}")
            st.write(f"Capacity: {current_product['capacity']}")
            st.write(f"Energy Rating: {current_product['energy_rating']}")
            st.write(f"Color: {current_product['color']}")
            
            st.write("**Features:**")
            for feature in current_product['features']:
                st.write(f"- {feature}")
    
    with col2:
        # Create a container with fixed height for the image and guessing section
        with st.container():
            # Load and resize product image
            image_path = f"data/images/{current_product['category']}/{current_product['id']}.jpg"
            if os.path.exists(image_path):
                resized_image = get_resized_image(image_path)
                if resized_image:
                    st.image(resized_image, caption=current_product['model'])
                else:
                    st.write("Error loading image")
            else:
                st.info(f"Placeholder image for {current_product['name']}")
            
            # Price guessing section
            with st.container():
                if not st.session_state.show_result:
                    st.subheader("Guess the Price!")
                    user_guess = st.number_input("Enter your price guess (in ₹):", 
                                               min_value=5000, 
                                               max_value=200000, 
                                               step=1000,
                                               key="price_input")
                    
                    if st.button("Submit Guess", key="submit_button"):
                        st.session_state.user_guess = user_guess
                        st.session_state.show_result = True
                        st.session_state.total_attempts += 1
                        
                        offer_price = current_product['offer_price']
                        difference = abs(offer_price - user_guess)
                        percentage_diff = (difference / offer_price) * 100
                        
                        if percentage_diff <= 10:
                            st.session_state.score += 1
                        
                        st.rerun()
                else:
                    offer_price = current_product['offer_price']
                    difference = abs(offer_price - st.session_state.user_guess)
                    percentage_diff = (difference / offer_price) * 100
                    
                    col_result1, col_result2, col_result3 = st.columns(3)
                    with col_result1:
                        st.write("**MRP:**")
                        st.write(f"₹{current_product['mrp']:,}")
                        st.write(f"Your savings: ₹{current_product['mrp'] - current_product['offer_price']:,}")
                    with col_result2:
                        st.write("**Offer Price:**")
                        st.write(f"₹{current_product['offer_price']:,}")
                        st.write("*Best deal!* 🏷️")
                    with col_result3:
                        st.write("**Your Guess:**")
                        st.write(f"₹{st.session_state.user_guess:,}")
                        difference_from_offer = abs(current_product['offer_price'] - st.session_state.user_guess)
                        st.write(f"Difference: ₹{difference_from_offer:,}")
                    
                    if percentage_diff <= 5:
                        st.success("Excellent! Within 5%! 🎯")
                    elif percentage_diff <= 10:
                        st.success("Great! Within 10%! 👍")
                    elif percentage_diff <= 20:
                        st.info("Not bad! Within 20%! 👌")
                    else:
                        st.error("Off by >20%! 🎲")
                    
                    st.write(f"Difference: ₹{difference:,} ({percentage_diff:.1f}%)")
                    
                    # Navigation buttons
                    if st.session_state.current_index < len(st.session_state.quiz_products) - 1:
                        if st.button("Next Product ➡️", key="next_button"):
                            st.session_state.current_index += 1
                            st.session_state.show_result = False
                            st.session_state.user_guess = None
                            st.rerun()
                    else:
                        st.success(f"Quiz completed! Score: {st.session_state.score}/{st.session_state.total_attempts}")
                        if st.button("Start Over 🔄", key="restart_button"):
                            products = load_json('data/products.json')['products']
                            st.session_state.quiz_products = random.sample(products, 2)
                            st.session_state.current_index = 0
                            st.session_state.show_result = False
                            st.session_state.user_guess = None
                            st.session_state.score = 0
                            st.session_state.total_attempts = 0
                            st.rerun()

    # Display score in sidebar
    st.sidebar.subheader("Score")
    st.sidebar.write(f"Correct Guesses (within 10%): {st.session_state.score}")
    st.sidebar.write(f"Total Attempts: {st.session_state.total_attempts}")
    
    # Display quiz progress
    progress = (st.session_state.current_index + 1) / len(st.session_state.quiz_products)
    st.sidebar.progress(progress)
    st.sidebar.write(f"Product {st.session_state.current_index + 1} of {len(st.session_state.quiz_products)}")

def main():
    st.set_page_config(page_title="Samsung Smart Cafe Thanjavur Quiz", page_icon="☕", layout="wide")
    
    # Initialize session state for registration
    if 'is_registered' not in st.session_state:
        st.session_state.is_registered = False
        st.session_state.user_name = None
        st.session_state.user_mobile = None
    
    # Initialize quiz session state
    if 'quiz_products' not in st.session_state:
        # Initialize random products
        products = load_json('data/products.json')['products']
        st.session_state.quiz_products = random.sample(products, 2)
        st.session_state.current_index = 0
        st.session_state.user_guess = None
        st.session_state.show_result = False
        st.session_state.score = 0
        st.session_state.total_attempts = 0
    
    if not st.session_state.is_registered:
        show_registration()
    else:
        show_quiz()

if __name__ == "__main__":
    main()
