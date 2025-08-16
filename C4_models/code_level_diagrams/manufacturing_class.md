```mermaid
classDiagram
    %% --- Product / Stock ---
    class Product {
        <<Model>>
        +id: int
        +name: string
        +category: string
        +price: float
    }

    class Stock {
        <<Model>>
        +id: int
        +product_id: int
        +quantity: float
        +location: string
        +adjustStock()
    }

    class CafeBatch {
        <<Model>>
        +id: int
        +product_id: int
        +qty: float
        +expiry_date: date
        +outlet_id: int
    }

    Stock "1" --> "0..*" CafeBatch : tracks batches
    ManufacturingOrder "many" --> "0..*" Stock : consumes/produces
    ManufacturingOrder "many" --> "1" Product : produces

    %% --- Bill of Materials ---
    class BoM {
        <<Model>>
        +id: int
        +name: string
        +product_id: int
        +createBoM()
        +getIngredients()
    }

    class Ingredient {
        <<Model>>
        +id: int
        +name: string
        +unit: string
        +cost_per_unit: float
        +supplier_id: int
    }

    BoM "1" --> "0..*" Ingredient : contains
    BoM "1" --> "0..*" ManufacturingOrder : used by

    %% --- Manufacturing Order ---
    class ManufacturingOrder {
        <<Model>>
        +id: int
        +bom_id: int
        +status: string
        +startProduction()
        +completeProduction()
    }

    %% --- Routing / Operations ---
    class Routing {
        <<Model>>
        +id: int
        +work_order_id: int
        +operation: string
        +sequence: int
    }
    ManufacturingOrder "1" --> "0..*" Routing : follows

    %% --- Quality Checks ---
    class QualityCheck {
        <<Model>>
        +id: int
        +mo_id: int
        +check_point: string
        +result: string
        +logQCResult()
    }
    ManufacturingOrder "1" --> "0..*" QualityCheck : triggers QC

    %% --- Waste / Scrap ---
    class Waste {
        <<Model>>
        +id: int
        +ingredient_id: int
        +quantity: float
        +reason: string
    }
    Ingredient "1" --> "0..*" Waste : may produce

    %% --- Relationships to Supplier / Outlet ---
    class Supplier {
        <<Model>>
        +id: int
        +name: string
        +contact_info: string
    }
    Ingredient --> Supplier : sourced from

    class CoffeeOutlet {
        <<Model>>
        +id: int
        +name: string
        +location: string
    }
    CafeBatch --> CoffeeOutlet : stored at
