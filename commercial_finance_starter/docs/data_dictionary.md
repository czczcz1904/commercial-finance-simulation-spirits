# Data dictionary

All monetary amounts are VND. Volume fields ending in `_Cases` represent cases, not bottles. Each fact table has a defined grain; do not join facts directly to each other in Power BI.

## Dimension tables

| Table | Grain | Key fields | Purpose |
|---|---|---|---|
| `dim_date` | One row per calendar day in 2025 | `Date` | Date, year, quarter and month attributes. Fact tables use the first day of each month in `Month_Start`. |
| `dim_brand` | One row per brand | `Brand_ID` | Common brand filter for SKU- and brand-level facts. |
| `dim_product` | One row per SKU | `SKU_ID` | Brand, category, pack size, units per case, illustrative list price and standard cost. |
| `dim_region` | One row per region | `Region_ID` | North, Central and South. |
| `dim_channel` | One row per channel | `Channel_ID` | On-trade and Off-trade. |
| `dim_distributor` | One row per fictional distributor | `Distributor_ID` | Fictional distributor identity, region and tier. |
| `dim_retailer` | One row per fictional outlet | `Retailer_ID` | Fictional outlet, region and channel. |

## Fact tables

| Table | Grain | Main measures | Description |
|---|---|---|---|
| `fact_sellin` | Month × Distributor × SKU × Channel | Paid cases, FOC cases, Gross Sales, A&D, Net Sales, COGS, Gross Profit | Simulated manufacturer sales into distributor route-to-market allocations. FOC cases are physical shipments but do not generate Gross Sales. |
| `fact_depletion` | Month × Distributor × SKU × Channel | `Depletion_Cases` | Simulated distributor shipments to downstream On-trade / Off-trade outlets. It is not consumer sell-out. |
| `fact_inventory` | Month × Distributor × SKU | Opening, physical Sell-in, Depletion, adjustments, closing, average inventory, inventory days | Monthly distributor stock movement. Depletion is aggregated across channels at this grain. |
| `fact_budget` | Month × Brand × Region × Channel | Sales Budget, Volume Target, A&P Budget | Simulated monthly target and approved investment budget. |
| `fact_ap_actual` | Month × Brand × Region × Channel × Campaign | A&P Actual, budget, spend variance, budget utilization | Simulated campaign / activity spending. The budget is repeated at the matching reporting grain for convenient comparison; use the Budget table as the budget source of record in your model. |
| `fact_retail_price` | Month × Retailer × SKU | Observed price, reference RSP, price index | Simulated retail-price observations. `Source_Type` explicitly marks the records as synthetic. |

## Important field definitions

### Sell-in and Gross-to-Net

- `SellIn_Paid_Cases`: invoiced cases.
- `FOC_Cases`: free-of-charge cases shipped.
- `SellIn_Physical_Cases`: paid plus FOC cases; this drives inventory receipts.
- `Gross_Sales_VND`: paid cases × illustrative list price per case.
- `Off_Invoice_Discount_VND`, `Rebate_VND`, `Trade_Allowance_VND`: modeled A&D components.
- `Total_AD_VND`: sum of the three A&D components.
- `Net_Sales_VND`: Gross Sales − Total A&D.
- `COGS_VND`: physical cases shipped × illustrative standard cost per case.
- `Gross_Profit_VND`: Net Sales − COGS.

For this exercise, all three A&D components are assumed to be contra-revenue. Actual accounting treatment depends on the nature of the payment and the company's accounting policy.

### Inventory

`Closing_Inventory_Cases = Opening_Inventory_Cases + SellIn_Physical_Cases - Depletion_Cases + Inventory_Adjustments_Cases`.

`Inventory_Days` uses average opening/closing inventory divided by monthly depletion, multiplied by the number of days in the month. It is a simplified proxy, not a substitute for a company's official inventory-days methodology.

### Retail prices

- `Observed_Price_Per_Bottle_VND`: simulated observed outlet price per bottle.
- `Reference_RSP_Per_Bottle_VND`: simulated reference retail price per bottle.
- `Price_Index`: observed price ÷ reference price × 100.

A price index below 100 only indicates a modeled observed price below the modeled reference; it does not imply a policy breach.

## Known limitations

- All values are synthetic and not calibrated to real company results or market size.
- Channel-coded Sell-in represents a simulated commercial allocation, not a claim about the company's source-system data model.
- Depletion is distributor-to-outlet movement, not verified consumer sell-out.
- A&P actuals are not causally linked to incremental sales; do not claim causal campaign ROI from this dataset.
- Retail prices are modeled, not scraped from live retailers.
- The year 2025 is used solely to provide a complete 12-month learning period.
