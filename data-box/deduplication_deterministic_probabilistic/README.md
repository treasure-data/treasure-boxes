# Deterministic and probabilistic deduplication

----
## Overview

This project provides a solution to deterministically and probabilistically deduplicate a given dataset that has no reliable identifier.

----
## Implementation
1. Copy and paste this code into Treasure Workflows or run it with TD toolbelt.
2. Set your TD master key as the workflow secret.
3. Change the database and tables in the config/params.yaml file.

----
## Considerations

This project was developed for a Vietnamese automobile customer. Consider changing the cleanse.sql accordingly to normalize characters and the variables in the scripts to better suit your needs.

The probabilistic matching script (pm.py) uses multiprocessing, consider changing the settings according to your dataset size.

----
## Questions

Please feel free to reach out to apac-se@treasure-data.com with any questions you have about using this code.
