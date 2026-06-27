with stg as (
    select * from {{ ref('stg_earthquakes') }}
),

final as (
    select
        date(origin_time) as day,
        count(event_id) as events_count,
        avg(magnitude) as avg_magnitude,
        max(magnitude) as max_magnitude,
        count(*) filter (where tsunami_flag = 1) as tsunami_count,
        count(*) filter (where alert_level is not null) as alerted_count
    from stg
    group by day
    order by day ASC
)

select * from final