import time
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project='growth-training-app', location='us-central1')

# Generate a video from the Flow-generated image of coach passing ball to player
# Using the composite image as a reference frame
image = types.Image.from_file(location="flow_pass.png")

operation = client.models.generate_videos(
    model="veo-3.1-fast-generate-preview",
    prompt="Animate this basketball training scene. The basketball moves from left to right in slow motion through the dark space. Cinematic lighting, dramatic shadows, solid dark background, professional sports atmosphere, 4K quality",
    image=image,
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        number_of_videos=1,
        duration_seconds=8,
        enhance_prompt=True,
    ),
)

print("Video generation started. Polling for completion...")
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)
    print(f"Status: {operation.done}")

print(f"Operation result: {operation.result}")
print(f"Operation response: {operation.response}")
print(f"Operation error: {operation.error}")
print(f"Operation metadata: {operation.metadata}")

if operation.response and operation.response.generated_videos:
    generated_video = operation.response.generated_videos[0]
    video = generated_video.video
    if video.video_bytes:
        with open("hero_video.mp4", "wb") as f:
            f.write(video.video_bytes)
        print("Video saved as hero_video.mp4")
    else:
        print("No video bytes in response")
else:
    print("Video generation failed or was rejected.")
