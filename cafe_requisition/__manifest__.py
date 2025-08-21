{
"name": "Cafe Requisition",
"version": "1.0.0",
"summary": "Outlet→HQ requisition with approval and internal transfer generation",
"author": "Cafe ERP",
"license": "LGPL-3",
"depends": ["stock", "product", "coffee_chain"],
"data": [
"security/ir.model.access.csv",
"data/sequence.xml",
"views/requisition_views.xml"
],
"application": False,
}