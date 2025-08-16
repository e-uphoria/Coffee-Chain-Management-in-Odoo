```mermaid
classDiagram
    class Supplier {
        +id
        +name
        +contact_info
    }
    class RFQ {
        +id
        +supplier_id
        +date
        +status
    }
    class PurchaseOrder {
        +id
        +rfq_id
        +supplier_id
        +date
        +status
    }
    class Delivery {
        +id
        +po_id
        +expected_date
        +status
    }
    class Invoice {
        +id
        +po_id
        +amount
        +date
        +status
    }

    Supplier "1" --> "0..*" RFQ
    Supplier "1" --> "0..*" PurchaseOrder
    PurchaseOrder "1" --> "0..*" Delivery
    PurchaseOrder "1" --> "0..*" Invoice
