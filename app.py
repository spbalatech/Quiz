import streamlit as st
import json
import os
from PIL import Image

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

def main():
    st.set_page_config(page_title="Samsung Home Appliance Price Quiz", page_icon="🏠", layout="wide")
    
    st.title("Samsung Home Appliance Price Quiz")
    st.write("Guess the price of each product!")

    # Load products
    products = load_json('data/products.json')
    
    # Initialize session state
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
        st.session_state.user_guess = None
        st.session_state.show_result = False
        st.session_state.score = 0
        st.session_state.total_attempts = 0

    # Get current product
    washing_machines = products['washing_machines']
    current_product = washing_machines[st.session_state.current_index]
    
    # Create columns with custom widths
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("Product Details:")
        # Create a container for scrollable product details
        with st.container():
            st.write(f"Model: {current_product['model']}")
            st.write(f"Type: {current_product['type']}")
            st.write(f"Capacity: {current_product['capacity']}")
            st.write(f"Energy Rating: {current_product['energy_rating']}")
            st.write(f"RPM: {current_product['rpm']}")
            
            st.write("**Features:**")
            for feature in current_product['features']:
                st.write(f"- {feature}")
            
            st.write("**Wash Programs:**")
            for program in current_product['programs']:
                st.write(f"- {program}")
    
    with col2:
        # Create a container with fixed height for the image and guessing section
        with st.container():
            # Load and resize product image
            image_path = f"data/images/washing_machine/{current_product['id']}.jpg"
            if os.path.exists(image_path):
                resized_image = get_resized_image(image_path)
                if resized_image:
                    st.image(resized_image, caption=current_product['model'])
                else:
                    st.write("Error loading image")
            else:
                st.write("Image not found in washing_machine folder")
            
            # Price guessing section in a smaller container
            with st.container():
                if not st.session_state.show_result:
                    st.subheader("Guess the Price!")
                    user_guess = st.number_input("Enter your price guess (in ₹):", 
                                               min_value=20000, 
                                               max_value=100000, 
                                               step=1000,
                                               key="price_input")
                    
                    if st.button("Submit Guess", key="submit_button"):
                        st.session_state.user_guess = user_guess
                        st.session_state.show_result = True
                        st.session_state.total_attempts += 1
                        
                        actual_price = current_product['price']
                        difference = abs(actual_price - user_guess)
                        percentage_diff = (difference / actual_price) * 100
                        
                        if percentage_diff <= 10:
                            st.session_state.score += 1
                        
                        st.rerun()
                else:
                    actual_price = current_product['price']
                    difference = abs(actual_price - st.session_state.user_guess)
                    percentage_diff = (difference / actual_price) * 100
                    
                    col_result1, col_result2 = st.columns(2)
                    with col_result1:
                        st.write(f"**Your Guess:**\n₹{st.session_state.user_guess:,}")
                    with col_result2:
                        st.write(f"**Actual Price:**\n₹{actual_price:,}")
                    
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
                    if st.session_state.current_index < len(washing_machines) - 1:
                        if st.button("Next Product ➡️", key="next_button"):
                            st.session_state.current_index += 1
                            st.session_state.show_result = False
                            st.session_state.user_guess = None
                            st.rerun()
                    else:
                        st.success(f"Quiz completed! Score: {st.session_state.score}/{st.session_state.total_attempts}")
                        if st.button("Start Over 🔄", key="restart_button"):
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

if __name__ == "__main__":
    main()
