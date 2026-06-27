with stg as (
    select * from {{ ref('stg_earthquakes') }}
),

final as (
    select
        region,
        count(event_id) as events_count,
        avg(magnitude) as avg_magnitude,
        max(magnitude) as max_magnitude,
        avg(depth_km) as avg_depth_km
    from stg
    group by region
    order by region ASC
)

select * from final