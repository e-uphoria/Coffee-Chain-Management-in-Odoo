odoo.define('discuss_voip_call.contact_call', function (require) {
    "use strict";

    const rpc = require('web.rpc');

    $(document).on('click', '.o_contact_call_btn', function () {
        const target_extension = $(this).data('extension');
        rpc.query({
            model: 'voip.call',
            method: 'create_call',
            args: [{
                phone_number: target_extension,
                direction: 'outgoing',
            }],
        }).then(function (result) {
            if (result.status === "success") {
                console.log("Calling extension:", target_extension);
            } else {
                console.error("Call failed:", result);
            }
        });
    });
});
