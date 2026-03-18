{{ 
  config(
    materialized = 'emepheral',
    tags = ['int', 'sales', 'target']
  ) 
}}

with sales_agg as (

    select
        month,
        year,
        category_level_1,

        sum(net_revenue) as actual_revenue,
        sum(gross_revenue) as gross_revenue,
        sum(discount_value) as total_discount,

        sum(quantity) as total_quantity,
        count(distinct invoice_no) as total_orders

    from {{ ref('stg_sales_transaction') }}
    where is_valid_sale = true

    group by
        month,
        year,
        category_level_1

),

target as (

    -- giả định bảng target đã được clean sẵn
    select
        month,
        category_level_1,

        cast(target_revenue as numeric) as target_revenue,
        cast(target_profit as numeric) as target_profit

    from {{ ref('stg_sales_target_monthly') }}

)

select
    coalesce(s.month, t.month) as month,
    s.year,
    coalesce(s.category_level_1, t.category_level_1) as category_level_1,

    -- actual
    s.actual_revenue,
    s.gross_revenue,
    s.total_discount,
    s.total_quantity,
    s.total_orders,

    -- target
    t.target_revenue,
    t.target_profit,

    -- KPI
    safe_divide(s.actual_revenue, t.target_revenue) as achievement_pct,
    (s.actual_revenue - t.target_revenue) as revenue_variance,

    -- optional metrics
    safe_divide(s.actual_revenue, s.total_orders) as aov,
    safe_divide(s.total_discount, s.gross_revenue) as discount_rate

from sales_agg s

full outer join target t
    on s.month = t.month
    and s.category_level_1 = t.category_level_1