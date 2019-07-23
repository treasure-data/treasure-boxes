SELECT
  id AS contactid,
  concat_array(
    quantitative_features(
      array(
        "annualrevenue", "numberofemployees"
      ),
      rescale(
        IF(
          annualrevenue IS NULL,
          ${td.last_results.train_avg_annualrevenue},
          annualrevenue
        ),
        ${td.last_results.test_min_annualrevenue},
        ${td.last_results.test_max_annualrevenue}
      ),
      rescale(
        IF(
          numberofemployees IS NULL,
          ${td.last_results.train_avg_numberofemployees},
          numberofemployees
        ),
        ${td.last_results.test_min_numberofemployees},
        ${td.last_results.test_max_numberofemployees}
      )
    ),
    categorical_features(
      array(
        "role", "job", "leadsource", "country", "industry",
        "has_phone_number", "is_free_email", "owner"
      ),
      role, job, leadsource, country, industry,
      has_phone_number, is_free_email, owner
    )
  ) AS features,
  is_won
FROM
  samples_test_${task}
;
