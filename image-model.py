import requests, base64, streamlit as st
from PIL import Image
from io import BytesIO

invoke_url = "https://ai.api.nvidia.com/v1/genai/nvidia/consistory"
api_key = "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"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}
st.title("Text to Image model")
subject_prompt = st.text_input("Subject Description", "an old woman wearing a dress")
subject_tokens = [token.strip() for token in st.text_input("Subject Word(s)", "woman, dress").split(",")]
style_prompt = st.selectbox(
    "Enter Image Style",
    (
        "A hyper-realistic digital painting of",
        "A photo of",
        "A 3D animation of",
        "A watercolor illustration of",
        "neonpunk style of",
        "An old story illustration of"
    )
)

scene_prompt1 = st.text_input("Anchor Scene Prompt 1", "walking in the garden")
scene_prompt2 = st.text_input("Anchor Scene Prompt 2", "feeding birds in the square")
attention_dropout = st.slider("Attention Dropout", 0.01, 0.75, 0.5)
cfg_scale = st.slider("CFG Scale", 1.1, 9.0, 5.0)
same_initial_noise = st.selectbox("Same Initial Noise", (True, False))


payload = {
    "mode": 'init',
    "subject_prompt": subject_prompt,
    "subject_tokens": subject_tokens,
    "subject_seed": 43,
    "style_prompt": style_prompt,
    "scene_prompt1": scene_prompt1,
    "scene_prompt2": scene_prompt2,
    "negative_prompt": "",
    "attention_dropout":attention_dropout,
    "cfg_scale": cfg_scale,
    "same_initial_noise": same_initial_noise
}

if st.button("Gen Image"):

    response = requests.post(invoke_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()

    st.subheader("Generated Images")
    for idx, img_data in enumerate(data['artifacts']):
        img_base64 = img_data["base64"]
        img_bytes = base64.b64decode(img_base64)
        image = Image.open(BytesIO(img_bytes))
        st.image(image, caption=f"Image {idx + 1}", use_column_width=True)
else:
    st.wirte("May be an Error")
