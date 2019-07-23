Salesforce.com Predictive Analytics Template
===

**Predictive analytics**, a technique to analyze historical data and predict future events, clearly helps sales and marketing activity to improve their efficiency and effectiveness.

In the context of predictive analytics, this page introduces a way to find promising *lead*, *contact* and/or *opportunity* from your company's Salesforce.com (SFDC) data. In particular, seeking promising leads is commonly known as ***predictive lead scoring*** in these days.

## Overview

Here is an overview of what we try to tackle:

![workflow](./docs/img/workflow.png)

1. Import SFDC raw data to Treasure Data
2. Extract partial data into auxiliary tables
3. [Normalize human-generated job titles](https://blog.treasuredata.com/blog/2017/06/06/use-ai-to-cleanse-salesforce-job-title-data-in-treasure-data/)
4. Integrate transformed job titles with other attributes
5. Launch predictive analytics, and find out our potential customers for sales team

In this page, we mainly focus on **step 2** to **5**. In order to transfer your SFDC data to Treasure Data as **step 1**, you first need to refer to the following article: **[How to integrate Salesforce data with Treasure Data](https://docs.treasuredata.com/articles/data-connector-salesforce)**.

Note that you can skip **step 3** if you use [resources/title_mapping.csv](./resources/title_mapping.csv).

## Input

Since SFDC data has a wide variety of data, this workflow requires you to have at least five tables with the following schema:

### Table: `contact`

| Column name | Sample | Description |
|:---:|:---:|:---|
| `id` | 000000000CCCCCCCCC | SFDC unique contact ID |
| `name`| John Doe ||
| `title` | Software Engineer | Job title  |
| `leadsource`| Referral | How this contact was originally recorded as "lead" |
| `accountid`| 000000000AAAAAAAAA | SFDC unique account ID this contact belongs |
| `ownerid`| 000000000OOOOOOOOO | SFDC unique owner (user) ID of this contact |
| `email`|  john@company_x.com ||
| `phone`|  (111)111-1111 | Phone number 1 (main) |
| `mobilephone`| (222)222-2222 | Phone number 2 (mobile) |
| `homephone`| (333)333-3333 | Phone number 3 (home) |
| `otherphone`| (444)444-4444 | Phone number 4 (other)  |
| `assistantphone`| (555)555-5555 | Phone number 5 (assistant) |

### Table: `opportunitycontactrole`

| Column name | Sample | Description |
|:---:|:---:|:---|
| `opportunityid`| 000000000OOOOOOOOO | SFDC unique opportunity ID |
| `contactid`| 000000000CCCCCCCCC | SFDC unique contact ID of people who belong to this opportunity|
| `isprimary`| 1 | Whether this contact is primary contact of this opportunity (1), or not (0) |

### Table: `user`

| Column name | Sample | Description |
|:---:|:---:|:---|
| `id` | 000000000OOOOOOOOO | SFDC unique user ID |
| `alias` | boss | Alias of this user |

### Table: `account`

| Column name | Sample | Description |
|:---:|:---:|:---|
| `id`| 000000000AAAAAAAAA | SFDC unique account ID |
| `name`| Company X |  |
| `billingcountry`| United States ||
| `industry`| Technology ||
| `annualrevenue`| 8000000.0 | Annual revenue of this account  |
| `numberofemployees`| 200 | Number of employees of this account |

### Table: `opportunity`

| Column name | Sample | Description |
|:---:|:---:|:---|
| `id`      | 000000000OOOOOOOOO | SFDC unique opportunity ID |
| `accountid`| 000000000AAAAAAAAA | SFDC unique account ID associated with this opportunity |
| `ownerid`  | 000000000OOOOOOOOO | SFDC unique user ID owning this opportunity |
| `stagename`| 1.0 Identify | Opportunity stage |
| `isclosed` | 1 | If this opportunity is closed (1), or not (0) |
| `iswon`    | 0 | If this opportunity was successfully closed (1), or lost (0) |

**Note:** Some columns allow to be missing; for example, five different phone numbers do not necessarily have to be filled with valid numbers.

## Workflow

We prepared a workflow to prioritize each of **qualified lead** and **opportunity** by computing scores based on historical data.

- **Qualified lead:** Contacts who are not associated with any opportunities
	- To get a completely new chance from potential contacts
- **Opportunity** (a.k.a. "deal")
	- To realize which opportunity is the most likely to be successfully closed, and focus on the promising opportunity

```sh
$ td wf run setup # create DB and initial tables
$ td wf push sfdc-predictive-analytics # push and schedule workflow
$ td wf start sfdc-predictive-analytics predict --session now # manually launch the workflow
```

- [setup.dig](./setup.dig) - TD workflow to prepare for predictive analytics
- [predict.dig](./predict.dig) - TD workflow to find out promising **qualified lead** and **opportunity**
- [config/params.yml](./config/params.yml) - defines configurable parameters such as source and target DB name

## Output

The following tables suggest probability which indicates how this qualified lead or opportunity is likely to lead winning opportunity.

### Table: `prediction_qualified_lead`

| probability<br/>`double` | contactid<br/>`string`|  accountid<br/>`string` | country<br/>`string` | ... *(auxiliary columns)* |
|:---:|:---:|:---:|:---:|:---:|
|0.79 | 000000000CCCC11111 |  000000000AAAA11111 | Japan | ... |
|0.68 | 000000000CCCC22222 |  000000000AAAA22222 | United States | ... |
|0.54 | 000000000CCCC33333 | 000000000AAAA33333 | United States | ... |
|...|...|...|...|...|

### Table: `prediction_opportunity`

| probability<br/>`double` | contactid<br/>`string`|  opportunityid<br/>`string` | opportunity_stage<br/>`double` | ... *(auxiliary columns)* |
|:---:|:---:|:---:|:---:|:---:|
|0.85 | 000000000CCCC44444 |  000000000OOOO11111 | 3.0 | ... |
|0.73 | 000000000CCCC55555 |  000000000OOOO22222 | 0.1 | ... |
|0.66 | 000000000CCCC66666 | 000000000OOOO33333 | 1.0 | ... |
|...|...|...|...|...|

## Conclusion

Treasure Machine Learning and Workflow make predictive analytics more handy. Once `prediction_qualified_lead` and/or `prediction_opportunity` table has been created, you can connect the result with the other tools such as SFDC itself and BI tools.

[Contact us](https://www.treasuredata.com/contact_us) if you interested in [our paid consulting service](https://docs.treasuredata.com/articles/data-science-consultation).