```mermaid
classDiagram
    class SaleOrder {
        +Char name
        +Many2one customer_id
        +Many2one outlet_id
        +Many2one payment_method_id
        +One2many order_line
        +Float amount_total
        +Date order_date
        +Method _prepare_invoice()
        +Method action_confirm()
    }

    class SaleOrderLine {
        +Many2one order_id
        +Many2one product_id
        +Many2one menu_item_id
        +Char size
        +Char milk_type
        +Char syrup
        +Boolean extra_shot
        +Float price_unit
        +Integer product_uom_qty
        +Float price_subtotal
    }

    class AccountMove {
        +Char name
        +Many2one partner_id
        +Many2one outlet_id
        +Float amount_total
        +Selection state
    }

    class AccountPayment {
        +Char name
        +Many2one partner_id
        +Many2one outlet_id
        +Many2one payment_method_id
        +Float amount
        +Selection state
    }

    class CoffeeMenuItem {
        +Char name
        +Selection status
        +Many2one product_id
    }

    %% Relationships
    SaleOrder "1" --> "many" SaleOrderLine : contains
    SaleOrder "1" --> "1" AccountMove : generates
    SaleOrder "1" --> "1" AccountPayment : linked
    SaleOrderLine "many" --> "1" CoffeeMenuItem : selects
    SaleOrder "1" --> "1" CoffeeMenuItem : product creation (if missing)
    AccountMove "1" --> "1" AccountPayment : reconciled
