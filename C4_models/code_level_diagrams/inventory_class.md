```mermaid
classDiagram
    class CafeBatch {
        +name: Char
        +product_id: Many2one(cafe.product)
        +qty: Float
        +expiry_date: Date
        +outlet_id: Many2one(coffee.outlet)
        +is_expired: Boolean (computed)
        +_compute_is_expired()
        +create(vals)
    }

    class CafeProduct {
        +name: Char
        +category: Char
        +price: Float
    }

    class CoffeeOutlet {
        +name: Char
        +location: Char
    }

    CafeBatch --> CafeProduct : product_id
    CafeBatch --> CoffeeOutlet : outlet_id
