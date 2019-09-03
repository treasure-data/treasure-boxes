SELECT
  -- F-measure
  fmeasure(array_slice(predicted,0,size(actual)), actual) as fmeasure,
  -- Recall@k
  recall_at(predicted, actual) as recall,
  recall_at(predicted, actual, 2) as recall_at_2,
  -- Precision@k
  precision_at(predicted, actual) as `precision`,
  precision_at(predicted, actual, 2) as precision_at_2,
  -- MAP@k
  average_precision(predicted, actual) as average_precision,
  average_precision(predicted, actual, 2) as average_precision_at_2,
  -- AUC@k
  auc(predicted, actual) as auc,
  auc(predicted, actual, 2) as auc_at_2,
  -- MRR@k
  mrr(predicted, actual) as mrr,
  mrr(predicted, actual, 2) as mrr_at_2,
  -- NDCG@k
  ndcg(predicted, actual) as ndcg,
  ndcg(predicted, actual, 2) as ndcg_at_2
FROM
  rf_topk_predict
