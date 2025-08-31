# -*- coding: utf-8 -*-
import logging
import base64
import hmac
import hashlib
import requests

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


def _hmac_b64(secret: str, message: str) -> str:
    dig = hmac.new(secret.encode("utf-8"), msg=message.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode("utf-8")


class EsewaController(http.Controller):
    # Success redirect (user browser)
    @http.route(['/payment/esewa/return'], type='http', auth="public", csrf=False)
    def esewa_return(self, **data):
        _logger.info("eSewa /return GET data: %s", data)
        # Typical params from eSewa after success: refId, oid, amt
        tx = request.env['payment.transaction'].sudo()._esewa_tx_from_return(data)
        tx._process_post_return(data)
        return request.redirect('/payment/status')

    # Failure/cancel redirect (user browser)
    @http.route(['/payment/esewa/cancel'], type='http', auth="public", csrf=False)
    def esewa_cancel(self, **data):
        _logger.info("eSewa /cancel data: %s", data)
        tx = request.env['payment.transaction'].sudo()._esewa_tx_from_return(data, ignore_missing=True)
        if tx:
            tx._set_canceled()
        return request.redirect('/payment/status')

    # Server-to-server verification (IPN-style) – optional, used by our return handler too
    @http.route(['/payment/esewa/verify'], type='json', auth="public", csrf=False)
    def esewa_verify(self, **payload):
        """Allows client-side (POS/JS) to request verification via Odoo server."""
        _logger.info("eSewa /verify payload: %s", payload)
        tx_ref = payload.get("reference")
        if not tx_ref:
            return {"ok": False, "error": "Missing reference"}

        tx = request.env['payment.transaction'].sudo().search([('reference', '=', tx_ref)], limit=1)
        if not tx:
            return {"ok": False, "error": "Transaction not found"}

        ok, info = tx._esewa_verify_with_gateway()
        return {"ok": ok, "info": info}
