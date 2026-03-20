import requests

# No API key needed — uses free OpenStreetMap APIs + Google Maps search fallback
HEADERS = {"User-Agent": "DermAI-App/1.0 (skin-diagnostic-tool)"}


def find_nearby_doctors(pincode, disease):

    # ── Step 1: Convert pincode → lat/lng using Nominatim ──
    geo_url = (
        f"https://nominatim.openstreetmap.org/search"
        f"?postalcode={pincode}&country=India&format=json&limit=1"
    )

    try:
        geo_response = requests.get(geo_url, headers=HEADERS, timeout=10).json()
    except Exception:
        return _google_fallback(pincode)

    if not geo_response:
        return _google_fallback(pincode)

    lat = float(geo_response[0]["lat"])
    lng = float(geo_response[0]["lon"])
    area_name = geo_response[0].get("display_name", "").split(",")[0]

    # ── Step 2: Find dermatologists/clinics via Overpass API ──
    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json][timeout:25];
    (
      node["healthcare"="doctor"](around:8000,{lat},{lng});
      node["healthcare"="clinic"](around:8000,{lat},{lng});
      node["amenity"="clinic"](around:8000,{lat},{lng});
      node["amenity"="doctors"](around:8000,{lat},{lng});
      node["amenity"="hospital"](around:8000,{lat},{lng});
      node["healthcare"="hospital"](around:8000,{lat},{lng});
    );
    out body 10;
    """

    try:
        overpass_response = requests.post(
            overpass_url,
            data={"data": query},
            headers=HEADERS,
            timeout=30
        ).json()
        elements = overpass_response.get("elements", [])
    except Exception:
        elements = []

    doctors = []
    for place in elements[:5]:
        tags = place.get("tags", {})
        name = tags.get("name") or tags.get("operator")
        if not name:
            continue

        place_lat = place.get("lat")
        place_lng = place.get("lon")

        address_parts = list(filter(None, [
            tags.get("addr:housenumber"),
            tags.get("addr:street"),
            tags.get("addr:suburb"),
            tags.get("addr:city"),
        ]))
        address = ", ".join(address_parts) if address_parts else area_name or "Nearby"

        doctors.append({
            "name": name,
            "rating": tags.get("stars", "N/A"),
            "address": address,
            "phone": tags.get("phone", ""),
            "maps_link": f"https://www.google.com/maps/search/?api=1&query={place_lat},{place_lng}",
        })

    # ── Step 3: Always append Google Maps search links as guaranteed fallback ──
    google_links = _google_fallback(pincode, lat, lng)
    combined = doctors + google_links
    return combined[:5]


def _google_fallback(pincode, lat=None, lng=None):
    """
    Returns Google Maps search links — no API key needed.
    Opens Google Maps search directly in the browser.
    """
    if lat and lng:
        base = f"{lat},{lng}"
    else:
        base = f"{pincode}+India"

    return [
        {
            "name": "Search Dermatologists Nearby",
            "rating": "N/A",
            "address": f"Tap to open Google Maps near {pincode}",
            "phone": "",
            "maps_link": f"https://www.google.com/maps/search/dermatologist+near+{base}",
        },
        {
            "name": "Search Skin Clinics Nearby",
            "rating": "N/A",
            "address": f"Tap to open Google Maps near {pincode}",
            "phone": "",
            "maps_link": f"https://www.google.com/maps/search/skin+clinic+near+{base}",
        },
        {
            "name": "Search Skin Specialists Nearby",
            "rating": "N/A",
            "address": f"Tap to open Google Maps near {pincode}",
            "phone": "",
            "maps_link": f"https://www.google.com/maps/search/skin+specialist+near+{base}",
        },
    ]
