Perplexity home page

Search docs

Ctrl K

Search...

Navigation

Guides

Pricing

HomeGuidesAPI ReferenceChangelogSystem StatusFAQDiscussions

##### Guides

  * Initial Setup
  * Supported Models
  * Pricing
  * Rate Limits and Usage Tiers
  * Structured Outputs Guide
  * Prompt Guide
  * Perplexity Crawlers

Model| Input Tokens (Per Million Tokens)| Reasoning Tokens (Per Million Tokens)| Output Tokens (Per Million Tokens)| Price per 1000 searches  
---|---|---|---|---  
`sonar-deep-research`| $2| $3| $8| $5  
`sonar-reasoning-pro`| $2| -| $8| $5  
`sonar-reasoning`| $1| -| $5| $5  
`sonar-pro`| $3| -| $15| $5  
`sonar`| $1| -| $1| $5  
`r1-1776`| $2| -| $8| -  
  
`r1-1776` is an offline chat model that does not use our search subsystem

## 

​

Pricing Breakdown

Detailed Pricing Breakdown for Sonar Deep Research

**Input Tokens**

  1. Input tokens are priced at $2/1M tokens

  2. Input tokens comprise of Prompt tokens (user prompt) + Citation tokens (these are processed tokens from running searches)

**Search Queries**

  1. Deep Research runs multiple searches to conduct exhaustive research

  2. Searches are priced at $5/1000 searches

  3. A request that does 30 searches will cost $0.15 in this step.

**Reasoning Tokens**

  1. Reasoning is a distinct step in Deep Research since it does extensive automated reasoning through all the material it gathers during its research phase

  2. Reasoning tokens here are a bit different than the CoTs in the answer - these are tokens that we use to reason through the research material prior to generating the outputs via the CoTs.

  3. Reasoning tokens are priced at $3/1M tokens

**Output Tokens**

  1. Output tokens (Completion tokens) are priced at $8/1M tokens

**Total Price**

Your total price per request finally is a sum of the above 4 components

Detailed Pricing Breakdown for Sonar Reasoning Pro and Sonar Pro

**Input Tokens**

  1. Input tokens are priced at $2/1M tokens and $3/1M tokens respectively

  2. Input tokens comprise of Prompt tokens (user prompt) + Citation tokens (these are processed tokens from running searches)

**Search Queries**

  1. To give detailed answers, both the Pro APIs also run multiple searches on top of the user prompt where necessary for more exhaustive information retrieval

  2. Searches are priced at $5/1000 searches

  3. A request that does 3 searches will cost $0.015 in this step

**Output Tokens**

  1. Output tokens (Completion tokens) are priced at $8/1M tokens and $15/1M tokens respectively

**Total Price**

Your total price per request finally is a sum of the above 3 components

Detailed Pricing Breakdown for Sonar Reasoning and Sonar

**Input Tokens**

  1. Input tokens are priced at $1/1M tokens for both

  2. Input tokens comprise of Prompt tokens (user prompt)

**Search Queries**

  1. Each request does 1 search priced at $5/1000 searches

**Output Tokens**

  1. Output tokens (Completion tokens) are priced at $5/1M tokens and $1/1M tokens respectively

**Total Price**

Your total price per request finally is a sum of the above 2 components

Supported ModelsRate Limits and Usage Tiers
