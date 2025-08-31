# -*- coding: utf-8 -*-

import logging
from odoo import models

_logger = logging.getLogger(__name__)


class PaymentEsewaHelper(models.AbstractModel):
    _name = "payment.esewa.helper"
    _description = "eSewa Helper (placeholder for custom flows)"

    # You can place custom routines here if you later add capture/refund or SDK server hops.
    # Kept minimal now to mirror your Khalti structure.
