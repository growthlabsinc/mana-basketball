import time
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project='growth-training-app', location='us-central1')

# Generate a basketball training highlight video for Mana Basketball
# Using the coach image as a reference frame
image = types.Image.from_file(location="coach.png")

operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="A basketball coach in a gray Mana Basketball hoodie standing on a dark court, cinematic lighting, dramatic dark background with subtle orange and blue rim lighting, professional sports atmosphere, slow motion, 4K quality",
    image=image,
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        number_of_videos=1,
        duration_seconds=5,
        enhance_prompt=True,
    ),
)

print("Video generation started. Polling for completion...")
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)
    print(f"Status: {operation.done}")

generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save(location="hero_video.mp4")
print("Video saved as hero_video.mp4")
