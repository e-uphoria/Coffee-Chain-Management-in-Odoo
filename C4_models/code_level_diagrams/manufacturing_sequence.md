```mermaid
sequenceDiagram
    actor ProductionManager
    participant BoMModel as "BoM Model"
    participant IngredientModel as "Ingredient Model"
    participant ManufacturingOrder as "ManufacturingOrder Model"
    participant RoutingModel as "Routing Model"
    participant StockModel as "Stock Model"
    participant CafeBatchModel as "CafeBatch Model"
    participant QualityCheckModel as "QualityCheck Model"
    participant WasteModel as "Waste Model"
    participant SupplierModel as "Supplier Model"
    participant CoffeeOutletModel as "CoffeeOutlet Model"

    %% Step 1: Create Manufacturing Order
    ProductionManager->>BoMModel: Select BoM for product
    BoMModel->>IngredientModel: Get required ingredients
    IngredientModel-->>BoMModel: List of ingredients with qty
    BoMModel-->>ProductionManager: BoM details ready

    ProductionManager->>ManufacturingOrder: Create MO
    ManufacturingOrder-->>ProductionManager: MO created

    %% Step 2: Follow Routing / Operations
    ManufacturingOrder->>RoutingModel: Fetch routing steps
    RoutingModel-->>ManufacturingOrder: Routing steps returned
    ProductionManager->>RoutingModel: Perform operations step by step

    %% Step 3: Consume Ingredients and Update Stock
    ManufacturingOrder->>StockModel: Deduct ingredient quantities
    StockModel-->>ManufacturingOrder: Stock updated
    ManufacturingOrder->>CafeBatchModel: Create finished product batch
    CafeBatchModel-->>StockModel: Add batch to stock

    %% Step 4: Quality Check
    ManufacturingOrder->>QualityCheckModel: Trigger QC
    QualityCheckModel-->>ManufacturingOrder: QC results logged

    %% Step 5: Waste / Scrap Tracking
    ManufacturingOrder->>WasteModel: Log wastage of ingredients
    WasteModel-->>IngredientModel: Update ingredient usage

    %% Step 6: Supplier / Outlet Links
    IngredientModel->>SupplierModel: Reference supplier
    CafeBatchModel->>CoffeeOutletModel: Assign batch to outlet
