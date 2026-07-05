import os, sys, pathlib

# key from Mission Control's env
for line in open(r"D:\Stratum137\Projects\mission-control\.env.local"):
    if line.startswith("GEMINI_API_KEY="):
        os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()

from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
OUT = pathlib.Path(r"C:\Stratum137\Projects\stratum137-website\assets\img")
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    "Photorealistic editorial photograph, warm natural light blended with a subtle teal (#2DD4BF) "
    "accent glow, deep navy (#1E2761) shadow tones, premium modern magazine feel, shallow depth of field, "
    "authentic American small service business setting, candid and human, not stocky or staged. "
    "ABSOLUTELY NO text, letters, numbers, UI screenshots, logos, or watermarks anywhere in the image."
)

IMAGES = [
    ("outcome-calls.jpg", "4:3",
     "A relaxed HVAC business owner in his 50s having dinner with his family at home in the evening, "
     "genuinely present and unbothered, while on the kitchen counter in the soft background his work phone "
     "sits glowing with a gentle teal light halo, clearly being handled without him. The feeling: every call "
     "answered, even after hours, life reclaimed."),
    ("outcome-followup.jpg", "4:3",
     "A young homeowner on her porch looking pleasantly surprised at her phone seconds after submitting a "
     "service request, warm morning light, a teal glow from the screen — the feeling of an instant, personal "
     "reply arriving in under a minute."),
    ("outcome-schedule.jpg", "4:3",
     "A plumbing technician in branded-blank workwear smiling as he loads his van at sunrise, and beside the van "
     "a tablet propped on the passenger seat showing an abstract completely-full day schedule as colored teal "
     "blocks (no readable text) — the feeling of a booked-solid week with zero no-shows."),
    ("outcome-reviews.jpg", "4:3",
     "A delighted middle-aged customer at her front door warmly shaking hands with a service professional after "
     "a completed job, golden hour light, and floating softly bokeh-blurred in the background air a few glowing "
     "teal five-pointed stars — the feeling of five-star reviews accumulating on their own."),
    ("svc-assessment.jpg", "16:9",
     "Overhead view of a business owner's hands and a consultant's hands over a beautiful printed strategy "
     "roadmap on a workshop table — the roadmap is an elegant abstract layered diagram with teal and navy "
     "blocks and connecting lines (purely abstract shapes, no readable text), next to a coffee cup and "
     "work gloves. The feeling: finally, a clear plan."),
    ("svc-engine.jpg", "16:9",
     "A small business storefront office at night, owner gone home, and inside the dark office a desk setup "
     "glows calmly with teal light like a quiet engine room still working — phones, calendar, follow-ups "
     "represented as soft abstract light streams flowing between devices. The feeling: revenue being captured "
     "while you sleep."),
]

for name, ratio, prompt in IMAGES:
    print(f"generating {name} ...", flush=True)
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[prompt + " " + STYLE],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=ratio),
            ),
        )
        saved = False
        for part in resp.parts:
            if part.inline_data:
                img = part.as_image()
                # downscale for web + compress
                w, h = img.size
                maxw = 1600
                if w > maxw:
                    img = img.resize((maxw, int(h * maxw / w)))
                img.convert("RGB").save(OUT / name, "JPEG", quality=82, optimize=True)
                print(f"  saved {name} {img.size}", flush=True)
                saved = True
                break
        if not saved:
            print(f"  NO IMAGE for {name}: {[p.text for p in resp.parts if p.text]}", flush=True)
    except Exception as e:
        print(f"  ERROR {name}: {e}", flush=True)
print("done")
