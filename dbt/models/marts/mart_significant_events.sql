with stg as (
    select * from {{ ref('stg_earthquakes') }}
),

final as (
    select *
    from stg
    where magnitude >= 5.0 or alert_level is not null
)

select * from final