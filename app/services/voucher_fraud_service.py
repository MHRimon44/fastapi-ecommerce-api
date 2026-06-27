from app.providers.voucher_fraud_provider import voucher_fraud_provider
from app.schemas.voucher_fraud_schema import (
    VoucherFraudDetectData,
    VoucherFraudDetectRequest,
)


class VoucherFraudService:
    def detect_fraud(
        self,
        request: VoucherFraudDetectRequest,
    ) -> VoucherFraudDetectData:
        return voucher_fraud_provider.detect_fraud(request)


voucher_fraud_service = VoucherFraudService()
