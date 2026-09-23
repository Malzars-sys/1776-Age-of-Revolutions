# BUILD START 1776 — Logging calibration

## Result

The research-only target of **75** levels is replaced by a viability target of **235** levels from **458** current levels. No gameplay file is changed.

## Method

- Demand is calculated from the corrected target levels and their effective current PMs, or the building base PM for new historical rows.
- The static supply target is 115% of target-building wood inputs both by country where demonstrated capacity exists and globally through retained exporter capacity.
- Historical logging locations are the floor. Extra supply is retained only from existing effective logging locations, with historical states first and then the largest current forest centers.
- No new forest location is invented and no retained state exceeds its current effective level solely for calibration.
- This is viability, not autarky: coastal countries may rely on trade where their demonstrated forest base is insufficient.

## Explicit China/Japan check

- China: {'Market_or_Country': 'CHI', 'Historical_Target_Supply': '0.0', 'Calibrated_Target_Supply': '560.0', 'Estimated_Demand': '320.0', 'Coverage_Ratio': '1.750', 'Trade_Access': 'COASTAL_OR_PORT_ACCESS', 'Risk': 'LOW_STATIC_BUILDING_DEMAND', 'Runtime_Required': 'YES'}
- Japan: {'Market_or_Country': 'JAP', 'Historical_Target_Supply': '0.0', 'Calibrated_Target_Supply': '160.0', 'Estimated_Demand': '120.0', 'Coverage_Ratio': '1.333', 'Trade_Access': 'COASTAL_OR_PORT_ACCESS', 'Risk': 'LOW_STATIC_BUILDING_DEMAND', 'Runtime_Required': 'YES'}

## Limits requiring runtime

Population demand, subsistence wood output, throughput modifiers, workforce, construction queues, customs unions, prices and trade routes are dynamic. The country rows are market proxies; every market summary row therefore requires runtime validation. A low static risk means only that target-building demand has a 15% buffer.
