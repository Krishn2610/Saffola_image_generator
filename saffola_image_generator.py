import streamlit as st
from PIL import Image
from io import BytesIO
from google import generativeai as genai

# Setting the Gemini API key
genai.configure(api_key="GOOGLE_API_KEY")

# Load the fixed Saffola packet image
with open("saffola_packet.png", "rb") as f:
    saffola_image_data = f.read()

# Streamlit Page Config & Title
st.set_page_config(page_title="Saffola Oats Image Generator", layout="centered")
st.title("Saffola Oats Image Generator")

# Custom CSS - Simplified and refined for alignment
st.markdown("""
<style>
/* Style for the Generate button */
div.stButton > button {
    background-color: #ffcc00; /* yellow */
    color: black;
    border: none;
    border-radius: 6px;
    height: 40px;
    font-weight: 600;
    font-size: 14px;
    cursor: pointer;
    /* This is the key for alignment: adjust this value */
    margin-top: 26px; /* Increased margin-top to push it down */
}
/* Style for the Generate button on hover */
div.stButton > button:hover {
    color: black; /* Ensure text remains black on hover */
    background-color: #e6b800; /* Slightly darker yellow on hover for visual feedback */
}
/* Style for the Generate button on focus */
div.stButton > button:focus {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Target the internal input element within st.text_input on focus */
.stTextInput input:focus {
    outline: none !important; /* Remove the default outline */
    box-shadow: none !important; /* Remove any default box shadow */
    border: 1px solid #ccc !important; /* Set a subtle grey border on focus */
}

/* Target the container for the text input on focus (for robustness) */
[data-testid="stTextInput"] > div > div > input:focus {
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid #ccc !important;
}

/* Remove previous column-specific alignment CSS to avoid conflicts */
/* div[data-testid="column"] > div:has(div.stButton) {
    display: flex;
    align-items: flex-end;
    height: 100%;
}
div[data-testid="stVerticalBlock"] > div.element-container:has(div.stButton) {
    display: flex;
    align-items: flex-end;
} */

</style>
""", unsafe_allow_html=True)

# Keeps image persistent after download
if "generated_img" not in st.session_state:
    st.session_state.generated_img = None

# Input & Button on Same Row
# Removed vertical_alignment from st.columns as we're using margin-top on button
col1, col2 = st.columns([5, 1], gap="small")

with col1:
    user_prompt = st.text_input(
        "Write your description:",
        placeholder="e.g., Place the Saffola Oats packet on a wooden kitchen counter with fruits"
    )

with col2:
    # No extra `st.write` or `st.markdown` here, rely purely on CSS margin-top
    generate = st.button("Generate")

# Smaller, Centered Instruction
st.markdown(
    "<p style='text-align:center; font-size:13px; color:gray;'>⚠️ Include the exact phrase <b>'Saffola Oats'</b> in your description.</p>",
    unsafe_allow_html=True
)

# Show Example Prompts
st.markdown("#### 💡 Prompts You Can Try:")
st.markdown("""
- **Saffola Oats** packet placed on a picnic blanket in a park with greenery around 
- **Saffola Oats** packet on a breakfast table with sunlight coming through the window and a glass of milk
- Hrithik Roshan holding a **Saffola Oats** packet in a modern gym environment 
""")

# Generate Image if Button Clicked
if generate and user_prompt.strip():
    with st.spinner("⏳ Generating your image..."):
        system_prompt = (
            "This is the original Saffola Oats packet. Do not change, stylize, or reinterpret the packaging — "
            "preserve the branding, logo, shape, and color scheme exactly as shown in the reference image. "
            "The packet must always be clearly clearly visible in the scene. "
            "The text on the packet should not be distorted and must remain readable.\n\n"
            "When generating scenes that include people, ensure correct limb and hand placement, "
            "and natural human posture. Avoid any anatomical distortions, extra limbs, or unnatural gestures.\n\n"
            "Ensure the overall scene is visually coherent, with appropriate context, lighting, and perspective. "
            "The product should feel naturally integrated into the environment described by the user."
        )

        contents = [
            {"text": system_prompt + " " + user_prompt},
            {"inline_data": {"mime_type": "image/png", "data": saffola_image_data}}
        ]

        model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")
        response = model.generate_content(
            contents=contents,
            generation_config={"response_modalities": ["TEXT", "IMAGE"]}
        )

        for part in response.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                st.session_state.generated_img = Image.open(BytesIO(part.inline_data.data))

# Display image persistently if it exists
if st.session_state.generated_img:
    st.image(st.session_state.generated_img, caption="✅ Generated Image")

    # Download option
    buf = BytesIO()
    st.session_state.generated_img.save(buf, format="PNG")
    st.download_button(
        label="⬇️ Download Image",
        data=buf.getvalue(),
        file_name="saffola_generated_image.png",
        mime="image/png"
    )
