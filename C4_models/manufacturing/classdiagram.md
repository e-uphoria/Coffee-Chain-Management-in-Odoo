```mermaid
classDiagram
    class BoM {
        <<Model>>
        +id: int
        +name: string
        +ingredients: List~Ingredient~
        +product_id: int
        +createBoM()
        +getIngredients()
    }

    class ManufacturingOrder {
        <<Model>>
        +id: int
        +bom_id: int
        +status: string
        +startProduction()
        +completeProduction()
    }

    class QualityCheck {
        <<Model>>
        +id: int
        +mo_id: int
        +result: string
        +logQCResult()
    }

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

    BoM "1" -- "many" ManufacturingOrder : used by
    ManufacturingOrder "1" -- "1" QualityCheck : sends logs to
    ManufacturingOrder "many" -- "1" Product : linked to
    ManufacturingOrder "many" -- "many" Stock : consumes/produces
