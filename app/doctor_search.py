import requests

# No API key needed — uses free OpenStreetMap APIs
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
        return []

    if not geo_response:
        return []

    lat = float(geo_response[0]["lat"])
    lng = float(geo_response[0]["lon"])

    # ── Step 2: Find dermatologists using Overpass API ──
    # Searches within ~5km radius for healthcare=doctor or amenity=clinic
    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json][timeout:25];
    (
      node["healthcare"="doctor"]["speciality"="dermatology"](around:5000,{lat},{lng});
      node["amenity"="clinic"](around:5000,{lat},{lng});
      node["amenity"="doctors"](around:5000,{lat},{lng});
      node["healthcare"="skin_clinic"](around:5000,{lat},{lng});
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
    except Exception:
        return []

    elements = overpass_response.get("elements", [])

    doctors = []

    for place in elements[:5]:
        tags = place.get("tags", {})
        name = tags.get("name") or tags.get("operator")

        # Skip unnamed places
        if not name:
            continue

        place_lat = place.get("lat")
        place_lng = place.get("lon")

        address_parts = filter(None, [
            tags.get("addr:housenumber"),
            tags.get("addr:street"),
            tags.get("addr:suburb"),
            tags.get("addr:city"),
        ])
        address = ", ".join(address_parts) or "Address not available"

        maps_link = (
            f"https://www.google.com/maps/search/?api=1"
            f"&query={place_lat},{place_lng}"
        )

        doctors.append({
            "name": name,
            "rating": tags.get("stars", "N/A"),
            "address": address,
            "phone": tags.get("phone", ""),
            "maps_link": maps_link,
        })

    # ── Fallback: broader search if nothing found ──
    if not doctors:
        fallback_query = f"""
        [out:json][timeout:25];
        (
          node["amenity"="hospital"](around:8000,{lat},{lng});
          node["amenity"="clinic"](around:8000,{lat},{lng});
        );
        out body 5;
        """
        try:
            fb_response = requests.post(
                overpass_url,
                data={"data": fallback_query},
                headers=HEADERS,
                timeout=30
            ).json()

            for place in fb_response.get("elements", [])[:5]:
                tags = place.get("tags", {})
                name = tags.get("name")
                if not name:
                    continue

                place_lat = place.get("lat")
                place_lng = place.get("lon")

                address_parts = filter(None, [
                    tags.get("addr:street"),
                    tags.get("addr:city"),
                ])
                address = ", ".join(address_parts) or "Address not available"

                doctors.append({
                    "name": name,
                    "rating": "N/A",
                    "address": address,
                    "phone": tags.get("phone", ""),
                    "maps_link": f"https://www.google.com/maps/search/?api=1&query={place_lat},{place_lng}",
                })
        except Exception:
            pass

    return doctors