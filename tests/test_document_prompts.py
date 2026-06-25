from app.prompts.document_prompts import (
    build_purchase_order_parse_prompt,
    build_tech_pack_extract_prompt,
)


def test_build_purchase_order_parse_prompt_contains_required_schema():
    text = "PO Number: PO-1001\nBuyer: SaRa Lifestyle Ltd"

    prompt = build_purchase_order_parse_prompt(text)

    assert "PO-1001" in prompt
    assert '"po_number"' in prompt
    assert '"buyer_name"' in prompt
    assert '"items"' in prompt


def test_build_tech_pack_extract_prompt_contains_required_schema():
    text = "Style No: ST-9001\nFabric: Polyester 600D"

    prompt = build_tech_pack_extract_prompt(text)

    assert "ST-9001" in prompt
    assert '"style_no"' in prompt
    assert '"fabric"' in prompt
    assert '"measurements"' in prompt
