# Data Layer Profile API

----
## Overview

This project provides a solution to ingesting data from data layers (e.g. data coming from Adobe Experience Manager) residing on a frontend (e.g. customer's website), and on a subsequent PAPI call, we can fetch segment data from TD for near real-time (web) personalization.

----
## Implementation
1. Copy and paste this code into customer's GTM container as a new tag (recommended) or inject it into their website directly.
2. Change values for write-only API key, database, table, PAPI token and servlet host (if applicable).
3. If GTM, make sure to set up the correct triggering. Page view works well.

----
## Considerations

There is a more direct and efficient way to retrieve data from source applications, like AEM. However, that involves more development work on the client's side.

This solution relies on a servlet in the backend that translates segment ids to segment names using TD's Audience API. This step would become obsolete in the near future, since PAPI will send segment names as well by default.

----
## Questions

Please feel free to reach out to apac-se@treasure-data.com with any questions you have about using this code.
