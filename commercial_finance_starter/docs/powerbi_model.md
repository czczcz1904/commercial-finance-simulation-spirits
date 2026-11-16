# Power BI model setup

Import the CSV files from `data/raw/`. Rename tables consistently (for example, `dim_date` → `Dim_Date`, `fact_sellin` → `Fact_SellIn`). Set ID columns to Text, date columns to Date, VND columns to Whole Number, and percentages to Decimal Number or Percentage as appropriate.

## Recommended relationships

Use single-direction filtering from dimensions to facts, with one-to-many cardinality:

| One side (dimension) | Many side (fact) | Key |
|---|---|---|
| Dim_Date[Date] | Fact_SellIn[Month_Start] | Date |
| Dim_Date[Date] | Fact_Depletion[Month_Start] | Date |
| Dim_Date[Date] | Fact_Inventory[Month_Start] | Date |
| Dim_Date[Date] | Fact_Budget[Month_Start] | Date |
| Dim_Date[Date] | Fact_AP_Actual[Month_Start] | Date |
| Dim_Date[Date] | Fact_RetailPrice[Observation_Month] | Date |
| Dim_Brand[Brand_ID] | all six fact tables[Brand_ID] | Brand ID |
| Dim_Product[SKU_ID] | Fact_SellIn / Fact_Depletion / Fact_Inventory / Fact_RetailPrice[SKU_ID] | SKU ID |
| Dim_Region[Region_ID] | all six fact tables[Region_ID] | Region ID |
| Dim_Channel[Channel_ID] | Fact_SellIn / Fact_Depletion / Fact_Budget / Fact_AP_Actual / Fact_RetailPrice[Channel_ID] | Channel ID |
| Dim_Distributor[Distributor_ID] | Fact_SellIn / Fact_Depletion / Fact_Inventory[Distributor_ID] | Distributor ID |
| Dim_Retailer[Retailer_ID] | Fact_RetailPrice[Retailer_ID] | Retailer ID |

For Fact_Budget and Fact_AP_Actual, brand is at Brand level, not SKU level. Do not connect either table to Dim_Product. Use Dim_Brand for common brand slicing.

## Modeling notes

1. `Dim_Date[Date]` has one row per day. Fact dates are month-start dates and match the first day of each month.
2. `Fact_Inventory` is at Month × Distributor × SKU grain; its depletion is already summed across channels. Do not connect it to Dim_Channel.
3. `Fact_Budget` is at Month × Brand × Region × Channel grain.
4. `Fact_AP_Actual` has one simulated activity row at the same month/brand/region/channel grain. Its budget amount is repeated for reference; use the Budget fact as the official budget source in measures.
5. `Fact_SellIn` and `Fact_Depletion` are both at Month × Distributor × SKU × Channel grain. Do not join them directly to each other.
6. Use single-direction dimension-to-fact relationships. Avoid bidirectional relationships unless you have a clear reason and have checked for ambiguous filter paths.
7. Hide technical keys from report view after the model is validated. Format VND measures with thousand separators and no decimal places; format ratios as percentages.

## Suggested report pages

- **01 Executive Overview:** Net Sales, Budget Achievement, Gross Margin, Sell-in, Depletion, A&P utilization; monthly trend; brand and channel mix; Gross-to-Net waterfall.
- **02 Distribution & Inventory:** Sell-in vs Depletion trend; closing inventory; inventory days by distributor; distributor/SKU detail table.
- **03 Gross-to-Net & Investment:** A&D breakdown; G2N rate; A&P budget vs actual; contribution after A&P; variance commentary.
- **Optional 04 Retail Price:** Observed retail price and price index by SKU, retailer, region and channel.

## Reconciliation before publishing

- Gross Sales − Total A&D = Net Sales.
- Off-invoice discount + rebate + trade allowance = Total A&D.
- Opening Inventory + physical Sell-in − Depletion + adjustments = Closing Inventory.
- Fact_SellIn physical cases aggregated by Month/Distributor/SKU = Fact_Inventory Sell-in.
- Fact_Depletion cases aggregated by Month/Distributor/SKU = Fact_Inventory Depletion.
- Budget and actual should be compared at the same Month/Brand/Region/Channel grain.
