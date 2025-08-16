```mermaid
sequenceDiagram
    actor OutletManager
    participant CafeBatchModel as "CafeBatch Model"
    participant CafeProductModel as "CafeProduct"
    participant CoffeeOutletModel as "CoffeeOutlet"

    OutletManager->>CafeBatchModel: create(vals)
    CafeBatchModel->>CafeProductModel: check product exists
    CafeProductModel-->>CafeBatchModel: product ok / error
    CafeBatchModel->>CoffeeOutletModel: check outlet exists
    CoffeeOutletModel-->>CafeBatchModel: outlet ok / error
    CafeBatchModel->>CafeBatchModel: check qty >= 0
    CafeBatchModel-->>OutletManager: batch created / error
