# KPI dictionary and starter DAX

Create measures (not calculated columns) for aggregations. The measures below assume the table and column names in `data/raw/` are imported unchanged.

## Sales & Gross-to-Net

```dax
Gross Sales = SUM(Fact_SellIn[Gross_Sales_VND])
Total A&D = SUM(Fact_SellIn[Total_AD_VND])
Net Sales = [Gross Sales] - [Total A&D]
G2N Rate = DIVIDE([Total A&D], [Gross Sales])
Sell-in Cases = SUM(Fact_SellIn[SellIn_Paid_Cases])
FOC Cases = SUM(Fact_SellIn[FOC_Cases])
Physical Sell-in Cases = SUM(Fact_SellIn[SellIn_Physical_Cases])
COGS = SUM(Fact_SellIn[COGS_VND])
Gross Profit = [Net Sales] - [COGS]
Gross Margin % = DIVIDE([Gross Profit], [Net Sales])
Net Sales per Paid Case = DIVIDE([Net Sales], [Sell-in Cases])
```

## Budget and trade investment

```dax
Sales Budget = SUM(Fact_Budget[Sales_Budget_VND])
Sales Budget Variance = [Net Sales] - [Sales Budget]
Sales Budget Achievement % = DIVIDE([Net Sales], [Sales Budget])
A&P Budget = SUM(Fact_Budget[AP_Budget_VND])
A&P Actual = SUM(Fact_AP_Actual[AP_Actual_VND])
A&P Spend Variance = [A&P Actual] - [A&P Budget]
A&P Budget Utilization % = DIVIDE([A&P Actual], [A&P Budget])
A&P % Net Sales = DIVIDE([A&P Actual], [Net Sales])
Contribution after A&P = [Gross Profit] - [A&P Actual]
```

**Modeling warning:** Avoid summing `Fact_AP_Actual[AP_Budget_VND]` as the official budget source when the separate `Fact_Budget` table is used. Use `Fact_Budget[AP_Budget_VND]` for the budget measure. Check that relationships and filter context do not duplicate budget values.

## Distribution and inventory

```dax
Depletion Cases = SUM(Fact_Depletion[Depletion_Cases])
Closing Inventory Cases = SUM(Fact_Inventory[Closing_Inventory_Cases])
Average Inventory Cases = AVERAGE(Fact_Inventory[Average_Inventory_Cases])
Inventory Days (Selected Month) =
VAR AvgStock = SUM(Fact_Inventory[Average_Inventory_Cases])
VAR MonthlyDepletion = SUM(Fact_Inventory[Depletion_Cases])
VAR DaysInMonth = MAX(Fact_Inventory[Days_In_Month])
RETURN
    DIVIDE(AvgStock * DaysInMonth, MonthlyDepletion)
```

Use this card with a single month in filter context. For a multi-month trend, use the row-level `Fact_Inventory[Inventory_Days]` or calculate one monthly result per month; do not add monthly inventory-days values together.

## Suggested time intelligence

After marking `Dim_Date[Date]` as the model's date table:

```dax
Net Sales LY =
CALCULATE([Net Sales], SAMEPERIODLASTYEAR(Dim_Date[Date]))

Net Sales YoY % =
DIVIDE([Net Sales] - [Net Sales LY], [Net Sales LY])
```

The starter dataset contains one year only, so Last Year and YoY measures will be blank until you deliberately extend the generator to at least two years.
