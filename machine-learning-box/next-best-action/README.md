# Next Best Action Recommendation System

**High Level Overview** (Please refer to the "pics" folder for screenshot examples of each step)

This Workflow allows for SQL rule-based (deterministic) models as well as ML-based (probabilistic)  models for building Next Best Action recommendation systems in real-time.  The deterministic logic is executed via SQL code adding specific NBA attributes to users’ profiles via workflows in real-time, using page-views data coming from our JS SDK.  The workflow also adds additional custom attributes to the user_master table such as "channel_ad_response_percentile" or "activity_period_engagement_percentile". These percentile attributes are then used to train ML models and create Probabilistic NBA Segments to layer on top of the Deterministic rules for the execution of specific marketing strategies.  The Probabilistic ML models score customers on their propensity to engage with a certain ad/ channel - ex. Facebook, Mobile, Email etc. and their propensity to engage with an ad during a certain time period  - morning, evening etc.

Our NBA approach aims to answer three main questions - **What? Where? When?**

**NBA: What?**

The deterministic models typically answer the question  - **"What?"** (what is our next best marketing action to take against this particular user?) Ex. If user has added something to cart recently, but has not purchased yet, our system will add user to the **"abandoned_cart"** segment within the CDP in real time.  Our Next Best Action recommendation system will then recommend that we retarget this user more aggressively since they have recently shown a high intent to purchase.   The same could be done for many different marketing rules that can be predefined and customized by our clients within the workflow and attached as attributes to the user_master table.

**NBA: Where?**

After the "What" is determined for a particular user by a deterministic model, we then layer an ML predictive algorithm for Next Best Action, which typically answers the question - **"Where?"**  (What marketing channel might be the most effective for this user to drive them further down the funnel).  Users are scored on a daily basis by our ML algorithm based on their browsing and ad-response data and assigned a propensity score to engage with a certain channel - Social, Mobile, Email, Display etc. So, in the end our Next Best Action Recommendation System will tell you "What" specific marketing action to take against different segments of users in real time, and "Where" that marketing action is most likely to generate best results.

**NBA: When?**

The **"When?"** works similar to the “Where”, but looks at what marketing channel might be the most effective for this user to drive them further down the funnel.  Users are scored on a daily basis by our ML algorithm based on their browsing and timesamp of event data and assigned a propensity score to engage during a certain time period - morning, afternoon, evening, overnight etc.   

So, in the end our Next Best Action Recommendation  System will tell you **what** specific marketing action to take against different segments of users in real time, **where** and **when** that marketing action is most likely to generate best results. This allows you to spend your marketing budget strategically and efficiently at scale in real-time.  Think of this kind of like a trading algorithm that would tell you which stocks to buy and when/where to buy them, so you would optimize your ROI expectations in the long run given historical data and statistics to predict future performance. All of this logic can be customized by the client.

### How to customize workflow to different use cases using the custom Workflow variables below:

- you need two data tables to start building your Next-Best-Action Recommendation System - **user_master** and **pageviews**

-  **database** - enter name of your database in TD
-  **user_master_table** enter name of your original user_master table (default is "user_master")
-  **user_master_join_key** enter name of main join key between user master and pageviews (default is "td_client_id")
-  **timestamp_column** enter name of column with timestamp logs (most commonly "time")
-  **original_pageviews** enter name of original pageviews table (default is "pageviews")
-  **activity_table** enter name of updated pageviews table that your create_pageviews_time_of_day.sql code generates (this adds "morning", "afternoon", "evening", and "overnight" labels to each pageviews event based on original timestamp)
-  **activity_table_join_key** enter name of main join key between user master and pageviews (default is "td_client_id")
-  **enriched_user_master_table** enter name of your enriched user master table after custom deterministic and probabilistic attributes are added by our SQL code(default is "user_master_enriched")
-  **enriched_user_master_table_temp** enter name of temp table that allows each SQL query to update user_master_enriched table with new attributes (default is "user_master_enriched_temp")
-  **time_source_column** enter name of column in pageviews_time_of_day table that contains the activity_period names (default is set to "activity_period")
-  **utm_source_column** enter name of column that contains url string for each pageview event (default is "td_url")
-  **utm_param**  enter label for extracting utm_source from pageview url string (default is "utm_source")
-  **cart_url** enter the exact url for the cleint's landing page where user has added an item to cart (default is 'https://www.ecsite-example.com/cart')
-  **purchase_url**  enter the exact url for the cleint's confirmation page for where a user has confirmed a purchase - this could be customized to any desired event such as form_submission, account_creation etc. (default is 'https://www.ecsite-example.com/order-confirmation')
-  **session_length_hours** define your session length for cart_abandonment segment (default is 24 hours)
-  **nba_retarget_table** enter name for the nba_retarget_table, which assigns boolean 0 or 1 to users who have abandoned cart in current browsing session (default is "cart_abandon")
-  **nba_awareness_table** enter name for the nba_awareness_table, which assigns boolean 0 or 1 to users who have only visited client's site once or less times and didn't come through and ad click (default is "new_visitor_no_ads")

-  Variables above allow for customizing the rule-based logic and the session length of your deterministic segments to better suit your particular use cases. Changing the SQL code that creates the **nba_retarget** and the **nba_awareness** deterministic attributes can allow for further customization of the rules of your deterministic segments. Same applies to changing the SQL code to the **calculate_ad_response_percentile** and **calcualte_activity_percentile** queries to further customize the logic when necessary.

## Explanation of individual SQL queries:

-  **create_pageviews_time_of_day.sql** - takes timestamp and assigns each pageview event an activity_period such as **morning** = 6am - 12pm, **afternoon** = 12pm - 6pm, **evening** = 6pm - 12am, **overnight** = 12am - 6am
-  **cart_abandon_table.sql** - partitions pageviews table by session_id and td_client_id and assigns boolean 1 to users who have abandoned their cart in the current browsing session, meaning their td_url column contains the **cart_url** from the variables above, but **DOES NOT** contain the **purchase_url** from variables above.
-  **nba_awareness_table.sql** - assigns boolean 0 or 1 to users who have only visited client's site one or less times and didn't come through and ad click and creates a table grouped by td_client_id
-  **create_user_master_enriched.sql** - takes a copy of the user_master table and enriches it with a **nba_retarget** and **nba_awareness** attributes, which will be later used to create our deterministic NBA segments.
-  **load_distinct_days.sql** - looks at the activity_period column in the pageviews_time_of_day table and returns a table of distinct activity_periods and a variable_name column, which will be used in a for_loop DigDag function to assign each user an activity_period_ad_response_percentile custom attribute, based on how many times they have logged a pageview event during each of the four time periods - **morning, afternoon, evening, overnight**
-  **calculate_activity_percentile.sql** - loops through all the distinct activity_periods from previous query and counts the number of pageviews during each period and ranks users in a percentile_score ranking from 0-99 based on how many events they have logged compared to the rest of the users.
-  **load_distinct_utm_params.sql** -  looks at the td_url column in the pageviews_time_of_day table and returns a table of distinct utm_source labels and a variable_name column, which will be used in a for_loop DigDag function to assign each user an channel_ad_response_percentile custom attribute, based on how many times they have engaged with an ad from the given marketing channel - **Ex. Facebook, AdWords, Email or any other channel present in client's utm_tags**
-  **calculate_ad_response_percentile.sql** -  loops through all the distinct utm_source channels from previous query and counts the number of times each user had that channel in their utm_source section of the utm_tag and assigns a percentile_score ranking from 0-99 based on how many ads they have engaged with via each utm_source compared to the rest of the users.


## How to train ML Probabilistic Models in the TD UI using all the custom percentile scores:

**1. Create Channel_Affinity Segments** -  ex. for example for a **"Facebook_Affinity"** segment, select all users with facebook_ad_response_percentile attribute scores >= 70. Clients can change the threshold in the UI based on their rules.

**2. Create Activity_Period_Affinity Segments** - ex. for example for a **"Morning_Affinity"** segment, select all users with morning_activity_percentile attribute scores >= 70. Clients can change the threshold in the UI based on their rules.

**3. Train ML Models in the UI to assign propensity scores** - ex. select your **"Facebook_Affinity"** segment as the **Positive Sample** to get the propensity_to_engage_with_facebook score, then use Suggested_Features or add custom features on top of selected features.  Do the same for time_of_day_periods - ex. select your **"Morning_Affinity"** segment as the **Positive Sample** to get the propensity_to_engage_morning scores for all of your users.

**4.  Re-Build your Master Segment** -  this will add the ML model propensity scores as attributes to each user, so you can use them to create your final Next_Best_Action segments.

**5.  Create Probabilistic Segments** - create a segment by selecting the "Possibly" and "Likely" group from each ML model and include "Positive Sample" and name segment **"Likely_to_engage_Facebook"** or **"Likely_to_engage_Morning"**

**5.  Create Next Best Action Segment Folders** - apply custom filters and activate to designated channels for a full Next Best Action Campaign orchestration within the CDP UI

-  **Example:**   Look inside the "pics" folder for screenshots of a few Next Best Action campaign setups. Example of filter rules below:

1.  [Attribute filter] -  include profiles where **nba_retarget  = 1**  (Deterministic rule for getting all users who have abandoned cart in current browsing session)
2.  [Segment filter] - include profiles from the **"Likely_to_engage_Facebook"** segments
3.  [Segment filter] - include profiles from the **"High_Morning_Activity"** segments

-  You can call the above segment **"NBA_Retarget_Facebook_Morning"** and in your Activations tab - activate it via Facebook and set a schedule for it to syndicate to Facebook Audiences Manager every morning at 5:59am, so that you can start targeting those users from 6am - 12pm according to a frequency and recency of your choice. You can repeat the same process for building segments for all other channels that came from the utm_source section of the utm_tags and for all the other time_of_day_periods and activating accordingly to the designated channel and scheduling segment to be targeted with ads during the desired time period.
