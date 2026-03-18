{{
  config(
    materialized = 'table',
    partition_by = {
      "field": "month",
      "data_type": "string"
    },
    cluster_by = ["category_level_1"],
    tags = ['mart', 'sales', 'dashboard']
  )
}}

select
    month,
    year,
    category_level_1,

    -- actual
    actual_revenue,
    gross_revenue,
    total_discount,
    total_quantity,
    total_orders,

    -- target
    target_revenue,
    target_profit,

    -- KPI
    achievement_pct,
    revenue_variance,
    aov,
    discount_rate,

    -- debug / monitoring
    case 
        when target_revenue is null then 'Missing Target'
        when actual_revenue is null then 'No Sales'
        else 'OK'
    end as data_status

from {{ ref('int_sales_monthly_category_vs_target') }}