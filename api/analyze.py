import base64
import json
import os
from http.server import BaseHTTPRequestHandler

from google import genai
from google.genai import types


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                return self._json(500, {"detail": "GEMINI_API_KEY is missing in Vercel Environment Variables."})

            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 9_000_000:
                return self._json(400, {"detail": "Image request is empty or too large."})

            body = json.loads(self.rfile.read(length))
            image_b64 = body.get("image", "")
            mime_type = body.get("mime_type", "image/jpeg")
            quantity = float(body.get("quantity", 1))

            if mime_type not in ("image/jpeg", "image/png", "image/webp"):
                return self._json(400, {"detail": "Use a JPG, PNG, or WEBP image."})
            if not image_b64 or not (0.25 <= quantity <= 20):
                return self._json(400, {"detail": "Please provide a valid image and serving quantity."})

            image_bytes = base64.b64decode(image_b64, validate=True)
            client = genai.Client(api_key=api_key)
            prompt = (
                "Identify the main food in this image and estimate nutrition for ONE serving "
                "of the visible food. Return only JSON with keys: food (string), calories "
                "(number in kcal), protein (grams), carbs (grams), fat (grams). "
                "Use realistic approximate estimates; do not claim laboratory accuracy."
            )
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            result = json.loads(response.text)
            for key in ("calories", "protein", "carbs", "fat"):
                result[key] = round(float(result[key]) * quantity, 1)
            result["food"] = str(result.get("food", "Food estimate"))
            return self._json(200, result)
       except Exception as e:
    print("Food analysis error:", repr(e))
    return self._json(500, {"detail": str(e)[:500]})

    def do_GET(self):
        return self._json(405, {"detail": "Use POST to analyze a food image."})

    def _json(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)
