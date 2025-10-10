


## How to use "procurment" source
Load procurement_lines.csv as your fact table.
Load products_catalog.csv and suppliers.csv as dimensions (optional).

- Build measures:

        - Organic % (by weight) = SUMX(Organic * Volume)/SUM(Volume)

        - Plant share (by weight) = SUMX(Plant * Volume)/SUM(Volume)

        - Animal welfare % (only Is_Animal=True)

        - CO₂ total = SUM(CO2e_kg), CO₂ per kg =           
        - DIVIDE(SUM(CO2e_kg), SUM(Volume_kg_L))

        - Danish % = SUMX(Danish * Volume)/SUM(Volume)

- Visuals to showcase:

            - Stacked column: Volume by Category (color split: organic/non-organic).

           - Line: Organic % trend by month.

            Bar: Welfare % by animal family (Pork/Chicken/Beef/Veal).

            Donut: Fish methods (better vs less).

            Map or bar: FAO sub-areas share.

            Table: Supplier × Category × Volume × Organic % × Cost.