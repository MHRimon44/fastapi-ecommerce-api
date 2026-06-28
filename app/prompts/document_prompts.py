def build_purchase_order_parse_prompt(
    extracted_text: str,
) -> str:
    return f"""
You are an expert purchase order parser.

Extract structured purchase order data from the text below.

Rules:
- Return only valid JSON.
- Do not include markdown.
- If a field is missing, return null.
- items should be a list of important item/product/style/SKU lines.
- total_quantity should be an integer if available.

Text:
{extracted_text}

Return JSON only in this exact format:
{{
  "po_number": null,
  "buyer_name": null,
  "supplier_name": null,
  "order_date": null,
  "total_quantity": null,
  "items": []
}}
"""


def build_tech_pack_extract_prompt(
    extracted_text: str,
) -> str:
    return f"""
You are an expert garment and bag tech-pack parser.

Extract structured tech-pack data from the text below.

Rules:
- Return only valid JSON.
- Do not include markdown.
- If a field is missing, return null.
- measurements should be a list of measurement-related lines.

Text:
{extracted_text}

Return JSON only in this exact format:
{{
  "style_no": null,
  "buyer_name": null,
  "product_type": null,
  "fabric": null,
  "color": null,
  "size_range": null,
  "measurements": []
}}
"""
