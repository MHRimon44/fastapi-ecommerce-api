def test_index_document_success(client):
    response = client.post(
        "/rag/documents/index",
        json={
            "title": "Return Policy",
            "content": (
                "Customers can return products within 7 days after delivery. "
                "The product must be unused and include the original packaging."
            ),
            "source_type": "policy",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Document indexed successfully"
    assert body["data"]["document_id"]
    assert body["data"]["title"] == "Return Policy"
    assert body["data"]["chunks_count"] >= 1


def test_index_document_validation_error(client):
    response = client.post(
        "/rag/documents/index",
        json={
            "title": "A",
            "content": "short",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_search_document_success(client):
    client.post(
        "/rag/documents/index",
        json={
            "title": "Delivery Policy",
            "content": (
                "Delivery usually takes 3 to 5 business days inside Dhaka. "
                "Outside Dhaka delivery may take longer depending on courier service."
            ),
            "source_type": "policy",
        },
    )

    response = client.post(
        "/rag/search",
        json={
            "query": "delivery Dhaka courier",
            "top_k": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Search completed successfully"
    assert len(body["data"]) >= 1
    assert body["data"][0]["score"] > 0
    assert "Delivery Policy" == body["data"][0]["title"]


def test_ask_question_success(client):
    client.post(
        "/rag/documents/index",
        json={
            "title": "Voucher Policy",
            "content": (
                "Voucher discount can be applied during checkout. "
                "A voucher may have a minimum purchase amount and usage limit."
            ),
            "source_type": "policy",
        },
    )

    response = client.post(
        "/rag/ask",
        json={
            "question": "How can voucher discount be applied?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Answer generated successfully"
    assert "Voucher discount" in body["data"]["answer"]
    assert len(body["data"]["sources"]) >= 1


def test_search_without_relevant_result(client):
    response = client.post(
        "/rag/search",
        json={
            "query": "volcano astronomy telescope",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Search completed successfully"
    assert body["data"] == []
