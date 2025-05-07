
def extract_base64_image(response):
    def search_in_parts(parts):
        for part in parts:
            if isinstance(part, dict) and "image_url" in part:
                url = part["image_url"].get("url", "")
                if "base64" in url:
                    return url.split(",")[-1]
        return None

    # 1. content varsa ve listse (LLM output formatı)
    content = getattr(response, "content", None)
    if isinstance(content, list):
        b64 = search_in_parts(content)
        if b64:
            return b64

    # 2. direk response.content["parts"] varsa
    if isinstance(content, dict) and "parts" in content:
        b64 = search_in_parts(content["parts"])
        if b64:
            return b64

    # 3. fallback: tüm stringlerde base64 ara
    response_str = str(response)
    for line in response_str.splitlines():
        if "data:image" in line and "base64," in line:
            return line.split("base64,")[-1].split('"')[0]

    raise ValueError("Base64 görsel bulunamadı.")
