with source as (
    select * from {{ source('raw', 'earthquakes_raw') }}
),

renamed as (
    select
        raw_json ->> 'id' as event_id,
        (raw_json -> 'properties' ->> 'mag')::numeric as magnitude,
        split_part(raw_json -> 'properties' ->> 'place', ', ', -1) as region,
        to_timestamp((raw_json -> 'properties' ->> 'time')::bigint / 1000) as origin_time,
        (raw_json -> 'properties' ->> 'felt')::integer as felt_count,
        raw_json -> 'properties' ->> 'alert' as alert_level,
        (raw_json -> 'properties' ->> 'tsunami')::integer as tsunami_flag,
        (raw_json -> 'properties' ->> 'sig')::integer as significance,
        raw_json -> 'properties' ->> 'status' as status,
        raw_json -> 'properties' ->> 'magType' as magnitude_type,

        (raw_json -> 'geometry' -> 'coordinates' ->> 0)::numeric as longitude,
        (raw_json -> 'geometry' -> 'coordinates' ->> 1)::numeric as latitude,
        (raw_json -> 'geometry' -> 'coordinates' ->> 2)::numeric as depth_km
    from source
)

select * from renamed