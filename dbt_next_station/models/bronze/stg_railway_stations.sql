with source as (
  select * from {{ source('bronze_raw', 'railway_stations') }}
),

railway_stations as (
  select
    cast(id as bigint) as station_id,
    cast(lat as double) as latitude,
    cast(lon as double) as longitude,
    lower(type) as station_type
  from
    source
  )

select * from railway_stations
