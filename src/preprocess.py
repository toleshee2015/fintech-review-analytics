import pandas as pd
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# -------------------------
# Text preprocessing function
# -------------------------
def preprocess_text(
    text,
    remove_stopwords=True,
    lemmatize=True
):
    """
    Preprocess review text using spaCy.

    Steps:
    - Tokenization
    - Lowercasing
    - Stop-word removal
    - Punctuation removal
    - Optional lemmatization
    """

    # Handle missing values
    if pd.isna(text):
        return ""

    # Convert to lowercase
    text = str(text).lower()

    # Process text with spaCy
    doc = nlp(text)

    cleaned_tokens = []

    for token in doc:

        # Skip punctuation and spaces
        if token.is_punct or token.is_space:
            continue

        # Skip stopwords if enabled
        if remove_stopwords and token.is_stop:
            continue

        # Lemmatization
        if lemmatize:
            cleaned_tokens.append(token.lemma_)
        else:
            cleaned_tokens.append(token.text)

    # Join tokens back into string
    return " ".join(cleaned_tokens)


# -------------------------
# Main processing pipeline
# -------------------------
def preprocess_dataset(input_path, output_path):

    # Load dataset
    df = pd.read_csv(input_path)

    # Apply preprocessing
    df["cleaned_review"] = df["review"].apply(
        preprocess_text
    )

    # Save cleaned dataset
    df.to_csv(output_path, index=False)

    print(f"Processed dataset saved to: {output_path}")


# -------------------------
# Run script
# -------------------------
if __name__ == "__main__":

    preprocess_dataset(
        "data/processed/cbe_clean.csv",
        "data/processed/cbe_text_processed.csv"
    )