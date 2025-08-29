```mermaid
classDiagram
    %% Coffee Outlet Module - Class Diagram

    class CoffeeOutlet {
        +Integer id
        +String name
        +String location
        +String manager
        +String regional_manager
        +Many2one customer_id
        +Many2one lead_id
        +create(vals)
    }

    class ResPartner {
        +Integer id
        +String name
        +One2many coffee_outlet_ids
    }

    class CRMLed {
        +Integer id
        +String name
        +Many2one partner_id
        +Many2one coffee_outlet_id
        +String type
    }

    %% Relationships
    CoffeeOutlet "1" --> "0..1" ResPartner : customer_id
    CoffeeOutlet "1" --> "0..1" CRMLed : lead_id
    ResPartner "1" --> "0..*" CoffeeOutlet : coffee_outlet_ids
