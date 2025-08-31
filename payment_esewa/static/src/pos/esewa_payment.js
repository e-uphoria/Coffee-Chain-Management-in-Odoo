/** @odoo-module **/

import { registerPaymentMethod } from "@point_of_sale/app/store/pos_store";
import { _t } from "@web/core/l10n/translation";
import { jsonrpc } from "@web/core/network/rpc_service";

const EsewaPayment = {
    name: "eSewa",
    canUse: (pos, paymentMethod) => {
        return !!paymentMethod.esewa_use_terminal;
    },
    sendPaymentRequest: async (env, paymentMethod, order) => {
        // In a real flow, you would open a web popup or native SDK.
        // Here we just call our /payment/esewa/verify endpoint to simulate/confirm.
        try {
            const ref = order.uid || order.name;
            const result = await jsonrpc("/payment/esewa/verify", { reference: ref });
            if (result.ok) {
                return { confirmed: true, payload: result.info };
            } else {
                return { confirmed: false, error: result.error || _t("Verification failed.") };
            }
        } catch (e) {
            return { confirmed: false, error: e.toString() };
        }
    },
    finalize: async () => {
        return true;
    },
};

registerPaymentMethod("esewa", EsewaPayment);
