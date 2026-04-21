with railway_stations as (
  select * from {{ ref('stg_railway_stations') }}
),

railway_stations_h3 as (
  select
    *,
    h3_longlatash3(latitude, longitude, {{ var('h3_resolution') }}) as h3_index
  from railway_stations
)

select * from railway_stations_h3
