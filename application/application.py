import argparse
import gradio as gr
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import os

MODEL_PATHS = {
    "fine_tuned_model": r"crawler and data\src\preprocess data\adl_algorithm\fine_tuned_model.h5",
    "full_data_model": r"crawler and data\src\preprocess data\adl_algorithm\full_data_model.h5",
    "two_label_model": r"crawler and data\src\preprocess data\adl_algorithm\two_label_model.h5",
}

VECTORIZER_PATHS = {
    "full_data_model": r"crawler and data\src\preprocess data\adl_algorithm\tfidf_vectorizer.pkl",
    "fine_tuned_model": r"crawler and data\src\preprocess data\adl_algorithm\tfidf_vectorizer_fine_tuned.pkl",
    "two_label_model": r"crawler and data\src\preprocess data\adl_algorithm\tfidf_vectorizer_two_labels.pkl"
}


LABELS = {
    "fine_tuned_model": ["Fake News", "Extreme bias", "clickbait", "credible"],
    "full_data_model": ["Fake News", "Extreme bias", "clickbait", "credible"],
    "two_label_model": ["Not credible", "credible"], 
}

def load_resources(model_type):
    """Load the specified model and vectorizer."""

    if model_type not in MODEL_PATHS:
        raise ValueError(f"Invalid model type. Choose from: {list(MODEL_PATHS.keys())}")

    print(f"Loading model: {model_type}")

    model = load_model(MODEL_PATHS[model_type])

    vectorizer_path = VECTORIZER_PATHS[model_type]

    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"Vectorizer not found at: {vectorizer_path}")
    
    with open(vectorizer_path, "rb") as file:
        vectorizer = pickle.load(file)

    labels = LABELS[model_type]
    
    return model, vectorizer, labels

def predict_text(title, description, body, model, vectorizer, labels):
    """Perform inference using the specified model and inputs."""

    input_text = " ".join([title, description, body])
    
    input_tfidf = vectorizer.transform([input_text]).toarray()
    
    predictions = model.predict(input_tfidf)[0]
    
    result = {label: round(score, 3) for label, score in zip(labels, predictions)}
    predicted_labels = [label for label, score in result.items() if score > 0.5]
    
    return {
        "Predicted Labels": predicted_labels if predicted_labels else ["None"],
        "Confidence Scores": result,
    }

def main():
    parser = argparse.ArgumentParser(description="Run a Gradio app for news classification.")
    parser.add_argument(
        "--model_type",
        type=str,
        required=True,
        choices=["fine_tuned_model", "full_data_model", "two_label_model"],
        help="Specify which model to use: fine_tuned_model, full_data_model, or two_label_model.",
    )
    args = parser.parse_args()

    model, vectorizer, labels = load_resources(args.model_type)
    
    title_input = gr.Textbox(label="Title", placeholder="Enter the news title")
    description_input = gr.Textbox(label="Description", placeholder="Enter the news description")
    body_input = gr.Textbox(label="Body", placeholder="Enter the news body")

    outputs = gr.JSON(label="Prediction Results")

    demo = gr.Interface(
        fn=lambda title, desc, body: predict_text(title, desc, body, model, vectorizer, labels),
        inputs=[title_input, description_input, body_input],
        outputs=outputs,
        title=f"News Classification Demo ({args.model_type})",
        description="This demo classifies news articles into categories based on their content.",
    )
    
    demo.launch(share=True)

if __name__ == "__main__":
    main()
