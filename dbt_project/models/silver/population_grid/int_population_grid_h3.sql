select
  h3_pointash3(geom_wkb, {{ var('h3_resolution') }} as h3_index,
  sum(population_value) as total_population
from
  {{ ref('stg_population_grid') }}
group by 1
