```mermaid
classDiagram
    %% Coffee Outlet CRM Integration - CRM Focused Class Diagram

    class CrmLead {
        +Integer id
        +String name
        +String type
        +Many2one coffee_outlet_id
        +One2many coffee_outlet_ids
    }

    class CoffeeOutlet {
        +Integer id
        +String name
        +Many2one customer_id
        +Many2one lead_id
    }

    class ResPartner {
        +Integer id
        +String name
        +One2many coffee_outlet_ids
    }

    %% Relationships
    CrmLead "1" --> "0..1" CoffeeOutlet : coffee_outlet_id
    CrmLead "1" --> "0..*" CoffeeOutlet : coffee_outlet_ids
    CoffeeOutlet "1" --> "0..1" ResPartner : customer_id
    ResPartner "1" --> "0..*" CoffeeOutlet : coffee_outlet_ids

 
