# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import logging
import requests

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

HMAC_FIELDS = ("total_amount", "transaction_uuid", "product_code")


def hmac_b64(secret, message):
    dig = hmac.new(secret.encode("utf-8"), msg=message.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode("utf-8")


class ProviderEsewa(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
    selection_add=[('esewa', 'eSewa')],
    ondelete={'esewa': 'set default'}
    )


    # Credentials (test/live)
    esewa_merchant_id = fields.Char(string="Merchant / Service Code", help="eSewa Merchant ID (e.g., EPAYTEST)")
    esewa_secret_key = fields.Char(string="Secret Key (ePay v2)")
    esewa_token = fields.Char(string="Token")
    esewa_client_id = fields.Char(string="Client ID (SDK)")
    esewa_client_secret = fields.Char(string="Client Secret (SDK)")
    esewa_test_mode = fields.Boolean(string="Use UAT (Test)", default=True)

    def _esewa_endpoints(self):
        if self.esewa_test_mode:
            return {
                "init": "https://uat.esewa.com.np/epay/main",
                "verify": "https://uat.esewa.com.np/epay/transrec",
            }
        return {
            "init": "https://esewa.com.np/epay/main",
            "verify": "https://esewa.com.np/epay/transrec",
        }

    # -- Outgoing payload (redirect/POST) --
    def _esewa_prepare_tx_payload(self, tx):
        self.ensure_one()
        amount = "%.2f" % tx.amount
        product_code = self.esewa_merchant_id or "EPAYTEST"
        transaction_uuid = tx.reference

        payload = {
            "amt": amount,                          # required by eSewa (amount)
            "pdc": "0",                             # tax/charge fields (optional)
            "psc": "0",
            "txAmt": "0",
            "tAmt": amount,                         # total amount
            "pid": transaction_uuid,                # product/transaction id
            "scd": product_code,                    # service code (merchant id)
            "su": tx._get_processing_info()["return_url"],  # success URL
            "fu": tx._get_processing_info()["cancel_url"],  # failure URL
        }

        # ePay v2 signature (if required by your account)
        # Common format: "total_amount={tAmt}&transaction_uuid={pid}&product_code={scd}"
        signing_str = f"total_amount={payload['tAmt']}&transaction_uuid={payload['pid']}&product_code={payload['scd']}"
        if self.esewa_secret_key:
            payload["signature"] = hmac_b64(self.esewa_secret_key, signing_str)
            payload["signed_field_names"] = "total_amount,transaction_uuid,product_code"

        return payload

    # -- Server-to-server verification --
    def _esewa_verify(self, reference, amount):
        self.ensure_one()
        url = self._esewa_endpoints()["verify"]
        params = {
            "amt": "%.2f" % (amount),
            "rid": reference,   # eSewa refId (returned on success) – we also try with pid
            "pid": reference,   # fallback verification by pid (transaction_uuid)
            "scd": self.esewa_merchant_id or "EPAYTEST",
        }
        try:
            resp = requests.get(url, params=params, timeout=20)
            txt = (resp.text or "").lower()
            ok = "success" in txt and resp.status_code == 200
            return ok, {"status_code": resp.status_code, "body": resp.text}
        except Exception as e:
            _logger.exception("eSewa verify error")
            return False, {"error": str(e)}


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    esewa_ref_id = fields.Char("eSewa RefId")

    # Map return data → tx
    def _esewa_tx_from_return(self, data, ignore_missing=False):
        ref = data.get("pid") or data.get("oid") or data.get("transaction_uuid") or data.get("reference")
        tx = self.sudo().search([("reference", "=", ref)], limit=1)
        if not tx and not ignore_missing:
            raise ValidationError(_("eSewa: Transaction not found for reference %s") % ref)
        return tx

    def _get_specific_rendering_values(self, processing_values):
        """Called by Odoo during checkout to build provider-specific payload."""
        self.ensure_one()
        provider = self.provider_id
        if provider.code != "esewa":
            return super()._get_specific_rendering_values(processing_values)

        payload = provider._esewa_prepare_tx_payload(self)
        # Save return/cancel for controllers
        self._set_pending()
        return {
            "api_url": provider._esewa_endpoints()["init"],
            "payload": payload,
            "tx": self,
        }

    def _get_specific_processing_values(self, processing_values):
        """Provide return/cancel URLs for our templates & payload."""
        self.ensure_one()
        if self.provider_code != "esewa":
            return super()._get_specific_processing_values(processing_values)
        base = self.acquirer_id.get_base_url() if hasattr(self, "acquirer_id") else self.provider_id.get_base_url()
        return {
            "return_url": f"{base}/payment/esewa/return",
            "cancel_url": f"{base}/payment/esewa/cancel",
        }

    # Called by our controller after the browser returns
    def _process_post_return(self, data: dict):
        self.ensure_one()
        status = (data.get("status") or "").lower()
        ref_id = data.get("refId") or data.get("rid")
        if ref_id:
            self.sudo().write({"esewa_ref_id": ref_id})

        # Try verify with gateway
        ok, info = self._esewa_verify_with_gateway()
        if ok:
            self._set_done()
        else:
            # If explicit failure from eSewa
            if status == "failure":
                self._set_error(_("eSewa reported failure."))
            else:
                self._set_pending(_("Awaiting confirmation from eSewa."))

    def _esewa_verify_with_gateway(self):
        self.ensure_one()
        provider = self.provider_id
        if provider.code != "esewa":
            return False, {"error": "Not an eSewa transaction"}
        ref = self.esewa_ref_id or self.reference
        return provider._esewa_verify(reference=ref, amount=self.amount)
