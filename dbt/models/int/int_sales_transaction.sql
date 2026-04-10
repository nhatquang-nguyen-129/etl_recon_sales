{{
  config(
    materialized = 'emepheral',
    tags = [
        'stg', 
        'sales', 
        'transaction'
    ]
  )
}}

with base as (

    select *
    from {{ ref('stg_sales_transaction') }}

),

aggregated as (

    select
        transaction_date,
        category_level_1,

        sum(quantity) as total_quantity,

        sum(gross_revenue) as gross_revenue,
        sum(discount_value) as discount_value,
        sum(net_revenue) as net_revenue

    from base
    group by
        transaction_date,
        category_level_1

)

select * from aggregated