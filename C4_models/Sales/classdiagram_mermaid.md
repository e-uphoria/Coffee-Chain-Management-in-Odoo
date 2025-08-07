```mermaid
classDiagram
    class SalesOrder {
        +int id
        +int customer_id
        +date order_date
        +string status
        +float total_amount
        +createOrder()
        +confirmOrder()
        +cancelOrder()
    }

    class ProductLine {
        +int product_id
        +int quantity
        +float price
        +subtotal()
    }

    class Customer {
        +int id
        +string name
        +string email
    }

    SalesOrder "1" *-- "many" ProductLine : contains
    SalesOrder --> Customer : placed by
