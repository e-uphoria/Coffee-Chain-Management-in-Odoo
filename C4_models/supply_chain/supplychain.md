```mermaid

flowchart TD

%% ===== OUTLET =====
subgraph Outlet [Cafe Outlet]
  A1[POS Sale] --> A2[Menu Item BOM]
  A2 --> A3[Deduct raw materials from outlet stock]
  A4[Low stock alert: milk or beans] --> A5[Requisition request]
end

%% ===== HQ =====
subgraph HQ [HQ Supply Chain]
  B1[Requisition approval] --> B2[Purchase order to vendor]
  B1 --> B3[Internal transfer from HQ warehouse]
  B4[Forecasting and planning] --> B2
  B4 --> B3
end

%% ===== VENDOR =====
subgraph Vendor [Supplier]
  C1[Receive PO] --> C2[Deliver goods]
  C2 --> C3[Delivery to HQ warehouse]
end

%% ===== WAREHOUSE =====
subgraph Warehouse [Central and Outlet Warehouse]
  D1[Receive goods] --> D2[Update inventory]
  D2 --> D3[Distribute to outlets]
  D3 --> A3
end

%% ===== ACCOUNTING =====
subgraph Accounting [Accounting]
  E1[Vendor bills] --> E2[Payment processing]
  E3[Costing and wastage tracking] --> E4[Financial reports]
end

%% ===== CROSS-LINKS =====
A5 --> B1
B2 --> C1
C3 --> D1
B3 --> D3
D2 --> E3
B2 --> E1
