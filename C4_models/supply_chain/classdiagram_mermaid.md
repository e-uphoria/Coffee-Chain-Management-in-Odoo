```mermaid
classDiagram
    class BaseModel {
        <<Model>>
    }

    class StockPicking {
        <<Model>>
        +name
        +state
        +location_id
        +location_dest_id
        +move_lines
        +button_validate()
    }

    class StockMove {
        <<Model>>
        +product_id
        +quantity_done
        +_action_done()
    }

    class StockLocation {
        <<Model>>
    }

    class StockQuant {
        <<Model>>
        +product_id
        +location_id
        +quantity
    }

    StockPicking --|> BaseModel
    StockMove --|> BaseModel
    StockLocation --|> BaseModel
    StockQuant --|> BaseModel

    StockPicking "1" *-- "0..n" StockMove : contains
    StockMove --> StockLocation : source
    StockMove --> StockLocation : destination
