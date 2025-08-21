```mermaid
flowchart TD

%% ===== VENDORS =====
subgraph Vendors [Suppliers]
  V1[Coffee Beans Supplier]
  V2[Milk Supplier]
  V3[Packaging Supplier]
end

%% ===== HQ CENTRAL WAREHOUSE =====
subgraph HQ [HQ & Central Warehouse]
  H1[Receive Goods from Vendors]
  H2[Quality Check & Store Inventory]
  H3[Approve Outlet Requisitions]
  H4[Prepare Shipment for Outlets]
end

%% ===== OUTLETS =====
subgraph Outlets [Cafe Outlets]
  O1[Outlet A]
  O2[Outlet B]
  O3[Outlet C]
  O4[Outlet D]
end

%% ===== ACCOUNTING =====
subgraph Accounting [Accounting Dept.]
  A1[Vendor Bills]
  A2[Payments]
  A3[Outlet COGS & Wastage Reports]
end

%% ===== FLOW LINES =====
V1 --> H1
V2 --> H1
V3 --> H1
H1 --> H2
H2 --> H3
H3 --> H4
H4 --> O1
H4 --> O2
H4 --> O3
H4 --> O4
O1 --> H3
O2 --> H3
O3 --> H3
O4 --> H3
H1 --> A1
A1 --> A2
H2 --> A3
O1 --> A3
O2 --> A3
O3 --> A3
O4 --> A3
