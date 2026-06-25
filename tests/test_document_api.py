def upload_sample_purchase_order(client):
    content = b"""
PO Number: PO-1001
Buyer: SaRa Lifestyle Ltd
Supplier: ABC Accessories Ltd
Order Date: 2026-06-25
Item: Laptop Backpack
SKU: BAG-001
Quantity: 500
Quantity: 200
"""

    return client.post(
        "/documents/upload",
        files={
            "file": (
                "purchase_order.pdf",
                content,
                "application/pdf",
            )
        },
    )


def upload_sample_tech_pack(client):
    content = b"""
Style No: ST-9001
Buyer: SaRa Lifestyle Ltd
Product Type: Backpack
Fabric: Polyester 600D
Color: Black
Size Range: S-XL
Measurement Chest: 20
Measurement Length: 30
Shoulder: 15
"""

    return client.post(
        "/documents/upload",
        files={
            "file": (
                "tech_pack.pdf",
                content,
                "application/pdf",
            )
        },
    )


def test_upload_document_success(client):
    response = upload_sample_purchase_order(client)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Document uploaded successfully"
    assert body["data"]["original_filename"] == "purchase_order.pdf"
    assert body["data"]["file_id"]


def test_upload_document_invalid_file_type(client):
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "sample.txt",
                b"not a pdf",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Only PDF files are allowed"


def test_parse_purchase_order_success(client):
    upload_response = upload_sample_purchase_order(client)
    file_id = upload_response.json()["data"]["file_id"]

    response = client.post(
        "/documents/parse-purchase-order",
        json={
            "file_id": file_id,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Purchase order parsed successfully"
    assert body["data"]["document_type"] == "purchase_order"
    assert body["data"]["po_number"] == "PO-1001"
    assert body["data"]["buyer_name"] == "SaRa Lifestyle Ltd"
    assert body["data"]["supplier_name"] == "ABC Accessories Ltd"
    assert body["data"]["total_quantity"] == 700


def test_parse_purchase_order_document_not_found(client):
    response = client.post(
        "/documents/parse-purchase-order",
        json={
            "file_id": "00000000-0000-0000-0000-000000000000",
        },
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Document not found"


def test_extract_tech_pack_success(client):
    upload_response = upload_sample_tech_pack(client)
    file_id = upload_response.json()["data"]["file_id"]

    response = client.post(
        "/documents/extract-tech-pack",
        json={
            "file_id": file_id,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Tech pack extracted successfully"
    assert body["data"]["document_type"] == "tech_pack"
    assert body["data"]["style_no"] == "ST-9001"
    assert body["data"]["buyer_name"] == "SaRa Lifestyle Ltd"
    assert body["data"]["product_type"] == "Backpack"
    assert body["data"]["fabric"] == "Polyester 600D"
    assert body["data"]["color"] == "Black"
    assert body["data"]["size_range"] == "S-XL"
    assert len(body["data"]["measurements"]) >= 2
