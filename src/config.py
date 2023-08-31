class PARAMS:
  SEED = 47

  n_splits = 5

  lgb_params = {
              'boosting_type': 'gbdt',
              'objective': 'tweedie',
              'tweedie_variance_power': 1.1,
              'metric': 'mae',
              'subsample': 0.5,
              #'subsample_freq': 1,
              'learning_rate': 0.03,
              #'feature_fraction': 0.5,
              'max_bin': 100,
              'n_estimators': 1000,
              'boost_from_average': False,
              'verbose': -1,
          }

  params = {
    'boosting_type': 'gbdt',
    'metric': 'custom',
    'objective': 'tweedie',
    'n_jobs': -1,
    'seed': 47,
    'learning_rate': 0.1,
    'bagging_fraction': 0.75,
    'bagging_freq': 10,
    'colsample_bytree': 0.75}