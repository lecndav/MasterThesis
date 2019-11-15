# Notizen zu Resultate und Daten

## 20.10

transform_mdf.py erstellt. Tranformiert Signale mit VZ und filtert nur auf interessante (siehe source code). Dateigröße davor: 455624, danach: 307960.

### Resultate

8 Minuten 10 Fahrer >86%
xx Minuten 2,3 Fahrer >95%

## Random Forest Parameter tuning

Parameter auswahl

```conf
n_estimators = [300, 400, 500, 600, 650, 700, 800, 1000, 1200, 1300, 1350, 1400, 1500, 1600, 1800, 2000]
max_depth = [5, 7, 9, 10, 12, 13, 15, 17, 18]
min_samples_leaf = [1, 3, 4, 5, 6]
criterion = ['gini', 'entropy']
```

Exec: `python3 optimization/random_forest_params.py -i ... -o resultate/random_forest_params`

Resultate mit `python3 data_analysis/random_forest_params.py -i resultate/random_forest_params`

* Best Criterion is `gini`
* Best `min_samples_leaf` is `1` (data set `msl`)
* Best `n_estimators` are `600,50,1000`
* Best `max_depth` are `15`, `17`
* `n_estimators` bis 800 keine bessere genauigkeit, danach sogar abflachend und viel länegere dauer

Accuracy zwischen 87 und 89

## Random Forest Parameter detailed tuning

```conf
n_estimators = 600,50,1000
max_depth = 15,17
```

Exec: `python3 optimization/random_forest_params_detailed.py -i ... -o resultate/random_forest_params`

Resultate mit `python3 data_analysis/random_forest_params_detailed.py -i resultate/random_forest_params_detailed`

* Best `max_depth` is `17`
* Best `n_estimator` is `600`
