"""
Remove backgrounds from coach and player images using Google Imagen API.
Run after: gcloud auth application-default login
"""
from google import genai
from google.genai import types
from google.genai.types import RawReferenceImage, MaskReferenceImage

client = genai.Client(vertexai=True, project='growth-training-app', location='us-central1')


def remove_bg(input_path, output_path, label):
    print(f"Processing {label}...")
    img = types.Image.from_file(location=input_path)

    raw_ref = RawReferenceImage(
        reference_id=1,
        reference_image=img,
    )
    mask_ref = MaskReferenceImage(
        reference_id=2,
        config=types.MaskReferenceConfig(
            mask_mode='MASK_MODE_BACKGROUND',
            mask_dilation=0,
        ),
    )

    response = client.models.edit_image(
        model='imagen-3.0-capability-001',
        prompt='Solid pure black background, completely dark, no texture, color #0a0a0a',
        reference_images=[raw_ref, mask_ref],
        config=types.EditImageConfig(
            edit_mode='EDIT_MODE_INPAINT_INSERTION',
            number_of_images=1,
            output_mime_type='image/png',
        ),
    )

    if response.generated_images:
        response.generated_images[0].image.save(location=output_path)
        print(f"{label} saved to {output_path}")
    else:
        print(f"No image generated for {label}")


# Coach image
remove_bg(
    "/Users/tradeflowj/Downloads/Generated Image March 16, 2026 - 10_40PM (1).jpg",
    "coach.png",
    "Coach"
)

# Player image
remove_bg(
    "/Users/tradeflowj/Downloads/Generated Image March 16, 2026 - 10_40PM.jpg",
    "player.png",
    "Player"
)

print("\nDone! Both images saved with dark backgrounds matching the website.")
