
import mercadopago
from config import MERCADO_PAGO_ACCESS_TOKEN

sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

def gerar_link_pagamento(descricao="Produto X", preco=10.00):
    preference_data = {
        "items": [
            {
                "title": descricao,
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": preco
            }
        ]
    }
    preference_response = sdk.preference().create(preference_data)
    if "init_point" in preference_response.get("response", {}):
        return preference_response["response"]["init_point"]
    return "⚠️ Erro ao gerar link de pagamento."
