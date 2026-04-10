{{
  config(
    materialized = 'ephemeral',
    tags = [
        'stg', 
        'sales', 
        'transaction'
    ]
  )
}}

{% set raw_project = target.project %}
{% set raw_schema = 'kids_dataset_sales_transaction_raw' %}
{% set table_prefix = 'kids_table_erp_lsretail_sales_transaction_' %}

{% if execute %}

    {% set tables_query %}
        select table_name
        from `{{ raw_project }}.{{ raw_schema }}.INFORMATION_SCHEMA.TABLES`
        where table_name like '{{ table_prefix }}m______'
    {% endset %}

    {% set results = run_query(tables_query) %}
    {% set table_names = results.columns[0].values() if results is not none else [] %}

{% else %}
    {% set table_names = [] %}
{% endif %}


{% if table_names | length == 0 %}

select
    cast(null as string)  as store_id,
    cast(null as string)  as store_name,
    cast(null as string)  as invoice_no,

    cast(null as date)    as transaction_date,

    cast(null as int64)   as year,
    cast(null as string)  as month,

    cast(null as string)  as product_id,
    cast(null as string)  as product_name,

    cast(null as string)  as category_level_1,
    cast(null as string)  as category_level_2,

    cast(null as int64)   as quantity,

    cast(null as numeric) as gross_revenue,
    cast(null as numeric) as discount_value,
    cast(null as numeric) as net_revenue,

    cast(null as string)  as promotion_code,
    cast(null as string)  as promotion_name,
    cast(null as string)  as discount_type,
    cast(null as string)  as promotion_type,
    
where false


{% else %}

{% for table_name in table_names %}

select
    store_id,
    store_name,
    invoice_no,

    DATE(transaction_date) as transaction_date,

    EXTRACT(YEAR FROM DATE(transaction_date)) as year,
    FORMAT_DATE('%Y-%m', DATE(transaction_date)) as month,

    product_id,
    product_name,

    category_level_1,
    category_level_2,

    quantity,

    transaction_value as gross_revenue,
    discount_value,
    (transaction_value - discount_value) as net_revenue,

    promotion_code,
    promotion_name,
    discount_type,
    promotion_type,

from `{{ raw_project }}.{{ raw_schema }}.{{ table_name }}`

{% if not loop.last %} union all {% endif %}

{% endfor %}

{% endif %}