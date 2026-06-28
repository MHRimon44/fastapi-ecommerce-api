from fastapi import APIRouter, status, Depends

from app.schemas.erp_policy_schema import (
    ERPPolicyAskRequest,
    ERPPolicyAskResponse,
    ERPPolicyIndexRequest,
    ERPPolicyIndexResponse,
    ERPPolicySearchRequest,
    ERPPolicySearchResponse,
)
from app.services.erp_policy_service import erp_policy_service
from app.dependencies.auth_guard import require_authenticated_user


router = APIRouter(
    prefix="/knowledge/erp-policies",
    tags=["ERP Policy Knowledge"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.post(
    "/index",
    response_model=ERPPolicyIndexResponse,
    status_code=status.HTTP_201_CREATED,
)
def index_erp_policy(
    request: ERPPolicyIndexRequest,
) -> ERPPolicyIndexResponse:
    data = erp_policy_service.index_policy(request)

    return ERPPolicyIndexResponse(
        message="ERP policy indexed successfully",
        data=data,
    )


@router.post(
    "/search",
    response_model=ERPPolicySearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_erp_policies(
    request: ERPPolicySearchRequest,
) -> ERPPolicySearchResponse:
    data = erp_policy_service.search_policies(request)

    return ERPPolicySearchResponse(
        message="ERP policy search completed successfully",
        data=data,
    )


@router.post(
    "/ask",
    response_model=ERPPolicyAskResponse,
    status_code=status.HTTP_200_OK,
)
def ask_erp_policy(
    request: ERPPolicyAskRequest,
) -> ERPPolicyAskResponse:
    data = erp_policy_service.ask_policy_question(request)

    return ERPPolicyAskResponse(
        message="ERP policy answer generated successfully",
        data=data,
    )
