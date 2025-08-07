```mermaid
classDiagram
    class CoffeeOutlet {
        +Char name
        +Char location
        +Char manager
        +Many2one customer_id (res.partner)
        +Many2one lead_id (crm.lead)
        +create(vals)
    }

    class ResPartner {
        +One2many coffee_outlet_ids (coffee.outlet, customer_id)
    }

    class CrmLead {
        +Many2one coffee_outlet_id (coffee.outlet)
    }

    class SaleOrder {
        +Many2one outlet_id (coffee.outlet)
        +Selection service_type
        +Many2one payment_method_id (account.payment.method)
        +_prepare_invoice()
        +default_get(fields_list)
    }

    class AccountMove {
        +Many2one outlet_id (coffee.outlet)
        +Many2one payment_method_id (account.payment.method)
    }

    class AccountPayment {
        +Many2one outlet_id (coffee.outlet)
    }

    CoffeeOutlet "1" --> "0..*" CrmLead : creates and links lead
    ResPartner "1" --> "0..*" CoffeeOutlet : owns (customer ↔ outlets)
    CrmLead --> "1" CoffeeOutlet : inverse reference
    SaleOrder --> AccountMove : prepares invoice with outlet/payment info
    SaleOrder --> AccountPayment : references payment method
    AccountMove --> CoffeeOutlet : carries outlet_id
    AccountMove --> AccountPayment : shares payment context
