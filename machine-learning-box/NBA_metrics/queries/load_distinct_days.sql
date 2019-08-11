select  distinct concat('''',activity_period,'''') as activity_period,
activity_period||'_activity_percentile' as var_name
from  ${td.activity_table}
