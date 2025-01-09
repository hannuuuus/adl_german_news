import gradio as gr
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle

trained_model_path = r"adl_german_news\crawler and data\src\preprocess data\adl_algorithm\full_data_model.h5"
model = load_model(trained_model_path)
print(f"Model {model} successfully loaded.")

pickle_path = r"adl_german_news\crawler and data\src\preprocess data\adl_algorithm\tfidf_vectorizer.pkl"
with open(pickle_path, "rb") as file:
    vectorizer = pickle.load(file)

labels = ["Fake News", "Extreme bias", "clickbait", "credible"]

def predict_text(title, description, body):

    input_text = " ".join([title, description, body])
    
    input_tfidf = vectorizer.transform([input_text]).toarray()
    
    # inference
    predictions = model.predict(input_tfidf)[0]
    
    result = {label: round(score, 3) for label, score in zip(labels, predictions)}
    predicted_labels = [label for label, score in result.items() if score > 0.5]
    
    return {
        "Predicted Labels": predicted_labels if predicted_labels else ["None"],
        "Confidence Scores": result,
    }

# interface
title_input = gr.Textbox(label="Title", placeholder="Enter the news title")
description_input = gr.Textbox(label="Description", placeholder="Enter the news description")
body_input = gr.Textbox(label="Body", placeholder="Enter the news body")

outputs = gr.JSON(label="Prediction Results")

demo = gr.Interface(
    fn=predict_text,
    inputs=[title_input, description_input, body_input],
    outputs=outputs,
    title="Demo",
    description="This demo classifies news articles into categories such as Fake News, Extreme Bias, Clickbait, or Credible based on their content.",
)

# Launch 
if __name__ == "__main__":
    demo.launch(share=True)
