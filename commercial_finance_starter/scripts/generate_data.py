#!/usr/bin/env python3
"""Generate a reproducible synthetic commercial-finance dataset.

All amounts, prices, volumes, customers and business scenarios are fictional.
This is an independent learning project and is not affiliated with Pernod Ricard.
Uses only the Python standard library.
"""

from __future__ import annotations

import csv
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any

SEED = 20261116
YEAR = 2025
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
RNG = random.Random(SEED)

MONTH_SEASONALITY = {
    1: 1.18, 2: 0.86, 3: 0.96, 4: 0.98, 5: 0.94, 6: 0.96,
    7: 0.95, 8: 0.97, 9: 1.00, 10: 1.06, 11: 1.10, 12: 1.24,
}

REGIONS = [
    {"Region_ID": "NORTH", "Region_Name": "North", "Region_Multiplier": 1.08},
    {"Region_ID": "CENTRAL", "Region_Name": "Central", "Region_Multiplier": 0.78},
    {"Region_ID": "SOUTH", "Region_Name": "South", "Region_Multiplier": 1.18},
]
CHANNELS = [
    {"Channel_ID": "ON", "Channel_Name": "On-trade", "Channel_Multiplier": 0.44},
    {"Channel_ID": "OFF", "Channel_Name": "Off-trade", "Channel_Multiplier": 0.56},
]

# Illustrative product assumptions only; not actual company prices or costs.
PRODUCTS = [
    {"SKU_ID": "CHV12-700", "Brand": "Chivas Regal", "Category": "Scotch Whisky", "Product_Name": "Chivas Regal 12 700ml", "Bottle_Size_ML": 700, "Units_Per_Case": 6, "List_Price_Per_Case_VND": 7_800_000, "Standard_Cost_Per_Case_VND": 3_900_000, "Base_Cases": 82},
    {"SKU_ID": "CHV12-1000", "Brand": "Chivas Regal", "Category": "Scotch Whisky", "Product_Name": "Chivas Regal 12 1000ml", "Bottle_Size_ML": 1000, "Units_Per_Case": 6, "List_Price_Per_Case_VND": 10_800_000, "Standard_Cost_Per_Case_VND": 5_400_000, "Base_Cases": 43},
    {"SKU_ID": "BALF-700", "Brand": "Ballantine's", "Category": "Scotch Whisky", "Product_Name": "Ballantine's Finest 700ml", "Bottle_Size_ML": 700, "Units_Per_Case": 6, "List_Price_Per_Case_VND": 4_500_000, "Standard_Cost_Per_Case_VND": 2_250_000, "Base_Cases": 105},
    {"SKU_ID": "BALF-1000", "Brand": "Ballantine's", "Category": "Scotch Whisky", "Product_Name": "Ballantine's Finest 1000ml", "Bottle_Size_ML": 1000, "Units_Per_Case": 6, "List_Price_Per_Case_VND": 6_300_000, "Standard_Cost_Per_Case_VND": 3_150_000, "Base_Cases": 58},
    {"SKU_ID": "JAM-700", "Brand": "Jameson", "Category": "Irish Whiskey", "Product_Name": "Jameson Original 700ml", "Bottle_Size_ML": 700, "Units_Per_Case": 6, "List_Price_Per_Case_VND": 5_700_000, "Standard_Cost_Per_Case_VND": 2_850_000, "Base_Cases": 91},
    {"SKU_ID": "JAM-1000", "Brand": "Jameson", "Category": "Irish Whiskey", "Product_Name": "Jameson Original 1000ml", "Bottle_Size_ML": 1000, "Units_Per_Case": 6, "List_Price_Per_Case_VND": 8_100_000, "Standard_Cost_Per_Case_VND": 4_050_000, "Base_Cases": 49},
    {"SKU_ID": "ABS-700", "Brand": "Absolut", "Category": "Vodka", "Product_Name": "Absolut Vodka 700ml", "Bottle_Size_ML": 700, "Units_Per_Case": 12, "List_Price_Per_Case_VND": 3_600_000, "Standard_Cost_Per_Case_VND": 1_800_000, "Base_Cases": 115},
    {"SKU_ID": "ABS-1000", "Brand": "Absolut", "Category": "Vodka", "Product_Name": "Absolut Vodka 1000ml", "Bottle_Size_ML": 1000, "Units_Per_Case": 12, "List_Price_Per_Case_VND": 5_000_000, "Standard_Cost_Per_Case_VND": 2_500_000, "Base_Cases": 62},
]


def write_csv(filename: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {filename}")
    path = OUT / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Created {path.relative_to(ROOT)} ({len(rows):,} rows)")


def month_starts(year: int) -> list[date]:
    return [date(year, m, 1) for m in range(1, 13)]


def build_dimensions() -> dict[str, list[dict[str, Any]]]:
    start = date(YEAR, 1, 1)
    end = date(YEAR, 12, 31)
    dates = []
    current = start
    while current <= end:
        dates.append({
            "Date": current.isoformat(),
            "Year": current.year,
            "Quarter": f"Q{((current.month - 1) // 3) + 1}",
            "Month_Number": current.month,
            "Month_Name": current.strftime("%B"),
            "Month_Start": current.replace(day=1).isoformat(),
            "Day_Of_Month": current.day,
            "Day_Of_Week": current.strftime("%A"),
        })
        current += timedelta(days=1)

    distributors = []
    for region in REGIONS:
        prefix = {"NORTH": "N", "CENTRAL": "C", "SOUTH": "S"}[region["Region_ID"]]
        for i in range(1, 5):
            distributors.append({
                "Distributor_ID": f"DST-{prefix}-{i:02d}",
                "Distributor_Name": f"{region['Region_Name']} Distributor {i:02d}",
                "Region_ID": region["Region_ID"],
                "Distributor_Tier": "A" if i == 1 else ("B" if i in (2, 3) else "C"),
                "Status": "Active",
            })

    retailers = []
    for region in REGIONS:
        prefix = {"NORTH": "N", "CENTRAL": "C", "SOUTH": "S"}[region["Region_ID"]]
        for channel in CHANNELS:
            for i in range(1, 5):
                retailers.append({
                    "Retailer_ID": f"RTL-{prefix}-{channel['Channel_ID']}-{i:02d}",
                    "Retailer_Name": f"{region['Region_Name']} {channel['Channel_Name']} Outlet {i:02d}",
                    "Region_ID": region["Region_ID"],
                    "Channel_ID": channel["Channel_ID"],
                    "Retailer_Type": "Bar/Restaurant" if channel["Channel_ID"] == "ON" else "Retail Store",
                })

    brands = sorted({p["Brand"] for p in PRODUCTS})
    brand_rows = [
        {"Brand_ID": f"BR-{i:02d}", "Brand": brand, "Category_Group": next(p["Category"] for p in PRODUCTS if p["Brand"] == brand)}
        for i, brand in enumerate(brands, start=1)
    ]
    brand_id_lookup = {r["Brand"]: r["Brand_ID"] for r in brand_rows}
    product_rows = []
    for product in PRODUCTS:
        product_rows.append({**product, "Brand_ID": brand_id_lookup[product["Brand"]]})

    return {
        "dim_date": dates,
        "dim_brand": brand_rows,
        "dim_product": product_rows,
        "dim_region": [{k: v for k, v in r.items() if k != "Region_Multiplier"} for r in REGIONS],
        "dim_channel": [{k: v for k, v in c.items() if k != "Channel_Multiplier"} for c in CHANNELS],
        "dim_distributor": distributors,
        "dim_retailer": retailers,
    }


def build_facts(dims: dict[str, list[dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    products = dims["dim_product"]
    brand_id_lookup = {r["Brand"]: r["Brand_ID"] for r in dims["dim_brand"]}
    distributors = dims["dim_distributor"]
    retailers = dims["dim_retailer"]
    months = month_starts(YEAR)
    region_lookup = {r["Region_ID"]: r for r in REGIONS}
    channel_lookup = {c["Channel_ID"]: c for c in CHANNELS}

    sellin: list[dict[str, Any]] = []
    depletion: list[dict[str, Any]] = []
    inventory: list[dict[str, Any]] = []
    budget: list[dict[str, Any]] = []
    ap_actual: list[dict[str, Any]] = []
    retail_price: list[dict[str, Any]] = []

    # Indexes used for building budget/AP facts after transaction facts exist.
    actuals_by_brand_region_channel_month: dict[tuple, dict[str, float]] = defaultdict(lambda: {"net_sales": 0.0, "sellin_cases": 0.0, "depletion_cases": 0.0, "gross_sales": 0.0})
    sellin_index: dict[tuple, dict[str, Any]] = {}
    depletion_index: dict[tuple, dict[str, Any]] = {}

    # Generate Sell-in at Month x Distributor x SKU x Channel grain.
    for month in months:
        month_factor = MONTH_SEASONALITY[month.month]
        for dist in distributors:
            region = region_lookup[dist["Region_ID"]]
            for product in products:
                for channel in CHANNELS:
                    base = product["Base_Cases"] * region["Region_Multiplier"] * channel["Channel_Multiplier"]
                    dist_factor = 1.10 if dist["Distributor_Tier"] == "A" else (1.00 if dist["Distributor_Tier"] == "B" else 0.88)
                    noise = RNG.uniform(0.88, 1.12)
                    special_push = 1.42 if (dist["Distributor_ID"] == "DST-S-01" and month.month in (1, 2, 3, 4)) else 1.0
                    paid_cases = max(1, round(base * month_factor * dist_factor * noise * special_push))
                    foc_rate = RNG.uniform(0.005, 0.035)
                    foc_cases = max(0, round(paid_cases * foc_rate))

                    list_price = int(product["List_Price_Per_Case_VND"])
                    gross_sales = paid_cases * list_price
                    channel_discount = 0.085 if channel["Channel_ID"] == "OFF" else 0.055
                    # A deliberately higher discount scenario for one brand/channel in selected months.
                    if product["Brand"] == "Absolut" and channel["Channel_ID"] == "OFF" and month.month in (6, 7, 8):
                        channel_discount += 0.045
                    off_invoice_rate = max(0.01, channel_discount + RNG.uniform(-0.012, 0.012))
                    rebate_rate = RNG.uniform(0.008, 0.022)
                    trade_allowance_rate = RNG.uniform(0.004, 0.018)
                    off_invoice = round(gross_sales * off_invoice_rate)
                    rebate = round(gross_sales * rebate_rate)
                    trade_allowance = round(gross_sales * trade_allowance_rate)
                    total_ad = off_invoice + rebate + trade_allowance
                    net_sales = gross_sales - total_ad
                    standard_cost = int(product["Standard_Cost_Per_Case_VND"])
                    cogs = (paid_cases + foc_cases) * standard_cost
                    gross_profit = net_sales - cogs
                    key = (month.isoformat(), dist["Distributor_ID"], product["SKU_ID"], channel["Channel_ID"])
                    row = {
                        "Month_Start": month.isoformat(),
                        "Distributor_ID": dist["Distributor_ID"],
                        "Region_ID": dist["Region_ID"],
                        "SKU_ID": product["SKU_ID"],
                        "Brand_ID": product["Brand_ID"],
                        "Brand": product["Brand"],
                        "Channel_ID": channel["Channel_ID"],
                        "SellIn_Paid_Cases": paid_cases,
                        "FOC_Cases": foc_cases,
                        "SellIn_Physical_Cases": paid_cases + foc_cases,
                        "List_Price_Per_Case_VND": list_price,
                        "Gross_Sales_VND": gross_sales,
                        "Off_Invoice_Discount_VND": off_invoice,
                        "Rebate_VND": rebate,
                        "Trade_Allowance_VND": trade_allowance,
                        "Total_AD_VND": total_ad,
                        "Net_Sales_VND": net_sales,
                        "Standard_Cost_Per_Case_VND": standard_cost,
                        "COGS_VND": cogs,
                        "Gross_Profit_VND": gross_profit,
                    }
                    sellin.append(row)
                    sellin_index[key] = row

    # Depletion at Month x Distributor x SKU x Channel grain.
    # Distributor DST-S-01 has deliberately weak depletion in Jan-Apr to create inventory build-up.
    for row in sellin:
        month = date.fromisoformat(row["Month_Start"])
        depletion_rate = RNG.uniform(0.72, 0.96)
        if row["Distributor_ID"] == "DST-S-01" and month.month in (1, 2, 3, 4):
            depletion_rate *= 0.66
        if month.month in (10, 11, 12):
            depletion_rate *= 1.04
        cases = max(0, round(row["SellIn_Physical_Cases"] * depletion_rate))
        drow = {
            "Month_Start": row["Month_Start"],
            "Distributor_ID": row["Distributor_ID"],
            "Region_ID": row["Region_ID"],
            "SKU_ID": row["SKU_ID"],
            "Brand_ID": row["Brand_ID"],
            "Brand": row["Brand"],
            "Channel_ID": row["Channel_ID"],
            "Depletion_Cases": cases,
        }
        depletion.append(drow)
        depletion_index[(row["Month_Start"], row["Distributor_ID"], row["SKU_ID"], row["Channel_ID"])] = drow

        group_key = (row["Month_Start"], row["Brand"], row["Region_ID"], row["Channel_ID"])
        agg = actuals_by_brand_region_channel_month[group_key]
        agg["net_sales"] += row["Net_Sales_VND"]
        agg["sellin_cases"] += row["SellIn_Physical_Cases"]
        agg["gross_sales"] += row["Gross_Sales_VND"]
        agg["depletion_cases"] += cases

    # Inventory at Month x Distributor x SKU grain; depletion is summed over channels.
    for dist in distributors:
        for product in products:
            opening = RNG.randint(35, 100)
            for month in months:
                month_key = month.isoformat()
                matching_sellin = [r for r in sellin if r["Month_Start"] == month_key and r["Distributor_ID"] == dist["Distributor_ID"] and r["SKU_ID"] == product["SKU_ID"]]
                matching_depletion = [r for r in depletion if r["Month_Start"] == month_key and r["Distributor_ID"] == dist["Distributor_ID"] and r["SKU_ID"] == product["SKU_ID"]]
                sellin_cases = sum(r["SellIn_Physical_Cases"] for r in matching_sellin)
                depletion_cases = sum(r["Depletion_Cases"] for r in matching_depletion)
                adjustment = RNG.randint(-2, 3)
                available = max(0, opening + sellin_cases + adjustment)
                if depletion_cases > available:
                    depletion_cases = available
                    # Reallocate the capped total across channel rows while preserving total stock movement.
                    original = sum(r["Depletion_Cases"] for r in matching_depletion)
                    remaining = depletion_cases
                    for idx, drow in enumerate(matching_depletion):
                        if idx == len(matching_depletion) - 1:
                            drow["Depletion_Cases"] = remaining
                        else:
                            allocated = round(depletion_cases * drow["Depletion_Cases"] / original) if original else 0
                            drow["Depletion_Cases"] = min(allocated, remaining)
                            remaining -= drow["Depletion_Cases"]
                closing = available - depletion_cases
                avg_inventory = (opening + closing) / 2
                days_in_month = 31 if month.month in (1, 3, 5, 7, 8, 10, 12) else (28 if month.month == 2 else 30)
                inventory_days = round((avg_inventory / depletion_cases) * days_in_month, 1) if depletion_cases > 0 else None
                inventory.append({
                    "Month_Start": month_key,
                    "Distributor_ID": dist["Distributor_ID"],
                    "Region_ID": dist["Region_ID"],
                    "SKU_ID": product["SKU_ID"],
                    "Brand_ID": product["Brand_ID"],
                    "Brand": product["Brand"],
                    "Opening_Inventory_Cases": opening,
                    "SellIn_Physical_Cases": sellin_cases,
                    "Depletion_Cases": depletion_cases,
                    "Inventory_Adjustments_Cases": adjustment,
                    "Closing_Inventory_Cases": closing,
                    "Average_Inventory_Cases": round(avg_inventory, 1),
                    "Days_In_Month": days_in_month,
                    "Inventory_Days": inventory_days,
                })
                opening = closing

    # Budget is built at Month x Brand x Region x Channel grain.
    # It is a simulated target; achievement should vary around 100%.
    for month in months:
        for brand in sorted({p["Brand"] for p in products}):
            brand_skus = {p["SKU_ID"] for p in products if p["Brand"] == brand}
            for region in REGIONS:
                for channel in CHANNELS:
                    key = (month.isoformat(), brand, region["Region_ID"], channel["Channel_ID"])
                    agg = actuals_by_brand_region_channel_month[key]
                    achievement_assumption = RNG.uniform(0.91, 1.08)
                    sales_budget = round(agg["net_sales"] / achievement_assumption) if agg["net_sales"] else 0
                    volume_target = round(agg["sellin_cases"] / achievement_assumption) if agg["sellin_cases"] else 0
                    ap_rate = RNG.uniform(0.018, 0.045)
                    ap_budget = round(sales_budget * ap_rate)
                    budget.append({
                        "Month_Start": month.isoformat(),
                        "Brand_ID": brand_id_lookup[brand],
                        "Brand": brand,
                        "Region_ID": region["Region_ID"],
                        "Channel_ID": channel["Channel_ID"],
                        "Sales_Budget_VND": sales_budget,
                        "Volume_Target_Cases": volume_target,
                        "AP_Budget_VND": ap_budget,
                    })

                    spend_factor = RNG.uniform(0.82, 1.12)
                    # Selected over-budget investment cases for analysis.
                    if brand == "Chivas Regal" and region["Region_ID"] == "SOUTH" and channel["Channel_ID"] == "ON" and month.month in (5, 6, 7):
                        spend_factor = 1.22
                    if brand == "Absolut" and region["Region_ID"] == "NORTH" and channel["Channel_ID"] == "OFF" and month.month in (6, 7, 8):
                        spend_factor = 1.16
                    actual_spend = round(ap_budget * spend_factor)
                    activity_types = ["Trade Activation", "Point-of-Sale Visibility", "Consumer Engagement", "Channel Support"]
                    ap_actual.append({
                        "Campaign_ID": f"CMP-{month.year}{month.month:02d}-{brand[:3].upper()}-{region['Region_ID']}-{channel['Channel_ID']}",
                        "Month_Start": month.isoformat(),
                        "Brand_ID": brand_id_lookup[brand],
                        "Brand": brand,
                        "Region_ID": region["Region_ID"],
                        "Channel_ID": channel["Channel_ID"],
                        "Activity_Type": RNG.choice(activity_types),
                        "AP_Actual_VND": actual_spend,
                        "AP_Budget_VND": ap_budget,
                        "Spend_Variance_VND": actual_spend - ap_budget,
                        "Budget_Utilization_Pct": round(actual_spend / ap_budget * 100, 1) if ap_budget else None,
                    })

    # Retail prices at Month x Retailer x SKU grain.
    for month in months:
        for retailer in retailers:
            channel = channel_lookup[retailer["Channel_ID"]]
            region = region_lookup[retailer["Region_ID"]]
            for product in products:
                bottle_list_price = product["List_Price_Per_Case_VND"] / product["Units_Per_Case"]
                reference_rsp = round(bottle_list_price * (1.20 if channel["Channel_ID"] == "ON" else 1.12), -3)
                local_factor = RNG.uniform(0.92, 1.10)
                # A deliberately wider price-spread case for one region/category.
                if retailer["Region_ID"] == "NORTH" and product["Brand"] == "Absolut" and month.month in (6, 7, 8):
                    local_factor = RNG.uniform(0.84, 1.13)
                observed = round(reference_rsp * local_factor, -3)
                retail_price.append({
                    "Observation_Month": month.isoformat(),
                    "Retailer_ID": retailer["Retailer_ID"],
                    "Region_ID": retailer["Region_ID"],
                    "Channel_ID": retailer["Channel_ID"],
                    "SKU_ID": product["SKU_ID"],
                    "Brand_ID": product["Brand_ID"],
                    "Brand": product["Brand"],
                    "Observed_Price_Per_Bottle_VND": int(observed),
                    "Reference_RSP_Per_Bottle_VND": int(reference_rsp),
                    "Price_Index": round(observed / reference_rsp * 100, 1) if reference_rsp else None,
                    "Source_Type": "Synthetic scenario",
                })

    # Refresh depletion values in the fact table after any stock caps were applied.
    actuals_by_brand_region_channel_month = defaultdict(lambda: {"net_sales": 0.0, "sellin_cases": 0.0, "depletion_cases": 0.0, "gross_sales": 0.0})
    for row in sellin:
        key = (row["Month_Start"], row["Brand"], row["Region_ID"], row["Channel_ID"])
        agg = actuals_by_brand_region_channel_month[key]
        agg["net_sales"] += row["Net_Sales_VND"]
        agg["sellin_cases"] += row["SellIn_Physical_Cases"]
        agg["gross_sales"] += row["Gross_Sales_VND"]
    for row in depletion:
        key = (row["Month_Start"], row["Brand"], row["Region_ID"], row["Channel_ID"])
        actuals_by_brand_region_channel_month[key]["depletion_cases"] += row["Depletion_Cases"]

    return {
        "fact_sellin": sellin,
        "fact_depletion": depletion,
        "fact_inventory": inventory,
        "fact_budget": budget,
        "fact_ap_actual": ap_actual,
        "fact_retail_price": retail_price,
    }


def validate(dims: dict[str, list[dict[str, Any]]], facts: dict[str, list[dict[str, Any]]]) -> list[str]:
    checks: list[str] = []
    sellin = facts["fact_sellin"]
    depletion = facts["fact_depletion"]
    inventory = facts["fact_inventory"]

    # Unique grain checks.
    sellin_keys = [(r["Month_Start"], r["Distributor_ID"], r["SKU_ID"], r["Channel_ID"]) for r in sellin]
    depletion_keys = [(r["Month_Start"], r["Distributor_ID"], r["SKU_ID"], r["Channel_ID"]) for r in depletion]
    inventory_keys = [(r["Month_Start"], r["Distributor_ID"], r["SKU_ID"]) for r in inventory]
    assert len(sellin_keys) == len(set(sellin_keys)), "Duplicate grain in fact_sellin"
    assert len(depletion_keys) == len(set(depletion_keys)), "Duplicate grain in fact_depletion"
    assert len(inventory_keys) == len(set(inventory_keys)), "Duplicate grain in fact_inventory"
    checks.append("PASS | Unique fact grains: sell-in, depletion and inventory")

    # Gross-to-net arithmetic.
    for r in sellin:
        assert r["Gross_Sales_VND"] - r["Total_AD_VND"] == r["Net_Sales_VND"], "Gross-to-net mismatch"
        assert r["Off_Invoice_Discount_VND"] + r["Rebate_VND"] + r["Trade_Allowance_VND"] == r["Total_AD_VND"], "A&D component mismatch"
        assert r["COGS_VND"] == r["SellIn_Physical_Cases"] * r["Standard_Cost_Per_Case_VND"], "COGS mismatch"
    checks.append("PASS | Gross-to-Net and COGS calculations reconcile")

    # Inventory reconciliation.
    for r in inventory:
        expected = r["Opening_Inventory_Cases"] + r["SellIn_Physical_Cases"] - r["Depletion_Cases"] + r["Inventory_Adjustments_Cases"]
        assert expected == r["Closing_Inventory_Cases"], "Inventory roll-forward mismatch"
        assert r["Closing_Inventory_Cases"] >= 0, "Negative closing inventory"
    checks.append("PASS | Inventory roll-forward reconciles and closing stock is non-negative")

    # Dimension key coverage.
    distributor_ids = {r["Distributor_ID"] for r in dims["dim_distributor"]}
    sku_ids = {r["SKU_ID"] for r in dims["dim_product"]}
    channel_ids = {r["Channel_ID"] for r in dims["dim_channel"]}
    assert all(r["Distributor_ID"] in distributor_ids and r["SKU_ID"] in sku_ids and r["Channel_ID"] in channel_ids for r in sellin)
    checks.append("PASS | Fact foreign keys map to dimension tables")

    # Stock movement consistency between monthly inventory and detailed fact tables.
    sellin_sum = defaultdict(int)
    depletion_sum = defaultdict(int)
    for r in sellin:
        sellin_sum[(r["Month_Start"], r["Distributor_ID"], r["SKU_ID"])] += r["SellIn_Physical_Cases"]
    for r in depletion:
        depletion_sum[(r["Month_Start"], r["Distributor_ID"], r["SKU_ID"])] += r["Depletion_Cases"]
    for r in inventory:
        key = (r["Month_Start"], r["Distributor_ID"], r["SKU_ID"])
        assert sellin_sum[key] == r["SellIn_Physical_Cases"], "Sell-in vs inventory mismatch"
        assert depletion_sum[key] == r["Depletion_Cases"], "Depletion vs inventory mismatch"
    checks.append("PASS | Sell-in and depletion detail reconcile to inventory fact")
    return checks


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dims = build_dimensions()
    facts = build_facts(dims)

    for name, rows in dims.items():
        write_csv(f"{name}.csv", rows)
    for name, rows in facts.items():
        write_csv(f"{name}.csv", rows)

    checks = validate(dims, facts)
    report_path = ROOT / "docs" / "validation_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"Synthetic dataset validation | seed={SEED} | year={YEAR}\n" + "\n".join(checks) + "\n",
        encoding="utf-8",
    )
    print("\n".join(checks))
    print(f"Validation report: {report_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
