with source as (
  select * from {{ source('bronze_raw', 'population_grid') }}
),

population_grid as (
  select
    cast(geom_wkb as binary) as geom_wkb,
    cast(value as double) as population_value
  from
    source
  where
    value != -99999
)

select * from population_grid
