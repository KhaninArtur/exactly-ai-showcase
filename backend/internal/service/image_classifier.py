import io

import torch
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification

from internal.consts import BASE_MODEL_NAME, CLASSIFICATION_MODEL_NAME
from internal.db.models import AnimalType

# Load the feature extractor and model
feature_extractor = ViTImageProcessor.from_pretrained(BASE_MODEL_NAME)
model = ViTForImageClassification.from_pretrained(CLASSIFICATION_MODEL_NAME)


def classify_image(image_data: bytes) -> AnimalType:
    """Classify an image provided as a base64-encoded string."""
    # Load the image from bytes
    image = Image.open(io.BytesIO(image_data))

    # Preprocess the image
    inputs = feature_extractor(images=image, return_tensors="pt")

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Process outputs (0 is a cat, 1 is a dog)
    logits = outputs.logits
    predicted_class_id = logits.argmax(-1).item()
    return AnimalType(predicted_class_id)
