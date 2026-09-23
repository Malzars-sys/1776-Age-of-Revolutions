# BUILD START 1776 — Runtime bureaucracy calibration Wave 2

## Scope

This pass uses the user-supplied runtime balances. It does not reopen small or sparsely populated countries, military/naval sizing, the Serenissima setup, or historical building geography.

## Qing population first

Qing population changes from **366,405,602** to **272,424,314**. The core provincial targets follow the 1776 Cao Shuji/Jiang Tao series. Split game states share their historical province total proportionally, while every existing culture/religion share inside a state is preserved. Conservative supplements retain frontier populations omitted or incompletely represented by the registered provincial table.

Source: Cao Shuji/Jiang Tao 1776 provincial series, reproduced by Shanghai Jiao Tong University: https://history.sjtu.edu.cn/SJTU/JDHistory/kindeditor/Upload/file/20200709/202007090934348680000.pdf

## Qing incorporation

Four further states are de-incorporated: Formosa, Shengjing, Southern Manchuria and Northern Manchuria. These represent a recently conquered/weakly integrated island frontier and the separate Manchurian banner-general system. No additional China-proper core province is de-incorporated.

## Administration

Population and incorporation effects are applied before the Qing residual. China then receives 711 simple-organization levels distributed across fifteen administrative regions. Other countries use their currently active administrative PM: Russia and the Dutch East Indies therefore receive fewer physical levels because horizontal drawer cabinets produce 50 bureaucracy per level.

| TAG | Before | Admin levels added | Projected after | Decision |
|---|---:|---:|---:|---|
| CHI | -10200.0 | 711 | 52.9 | RUNTIME_CALIBRATION |
| KOR | -389.0 | 38 | -9.0 | RUNTIME_CALIBRATION |
| RUS | -588.0 | 12 | 12.0 | RUNTIME_CALIBRATION |
| PLC | -412.0 | 41 | -2.0 | RUNTIME_CALIBRATION |
| TUR | -660.0 | 65 | -10.0 | RUNTIME_CALIBRATION |
| POR | -261.0 | 26 | -1.0 | RUNTIME_CALIBRATION |
| USA | -557.0 | 55 | -7.0 | RUNTIME_CALIBRATION |
| SC1 | -589.0 | 58 | -9.0 | RUNTIME_CALIBRATION |
| SC2 | -217.0 | 21 | -7.0 | RUNTIME_CALIBRATION |
| BRZ | -307.0 | 30 | -7.0 | RUNTIME_CALIBRATION |
| PER | -109.0 | 10 | -9.0 | RUNTIME_CALIBRATION |
| VEN | -141.0 | 0 | -141.0 | PROTECTED_NO_CHANGE |
| DEI | -266.0 | 6 | 34.0 | RUNTIME_CALIBRATION |
| GWA | -40.7 | 4 | -0.7 | RUNTIME_CALIBRATION |
| MARATH | -153.0 | 15 | -3.0 | RUNTIME_CALIBRATION |
| PHI | 18.3 | 0 | 18.3 | NO_CHANGE_ALREADY_HEALTHY |

Venice remains at `-141` because VEN/GEN are protected. The Philippines receives no addition because its observed balance is already positive.

## Infrastructure follow-up

Administration changes are included in a fresh global infrastructure calculation. The cumulative runtime overlay adds **1110** Regional Infrastructure levels relative to the frozen historical matrix. Road/canal identity is preserved; active rail and passenger trains remain forbidden in 1776.

## Runtime caveat

Balances are projections from the supplied screenshots and scripted PM output. A new game is required to confirm employment, institution costs and exact rounding after the population history change.

## Validation targets

- China total population equals the state-by-state audit.
- All supplied deficits except protected Venice project to positive or only slightly negative.
- No protected military/naval or Serenissima building placement changes.
- No active rail or passenger PM.
- The combined runtime matrix remains the validator authority.
