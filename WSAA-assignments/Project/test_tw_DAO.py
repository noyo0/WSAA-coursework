# My SQL commands for truckwash database
# datatable: tw_transactions
# sample:
#+-----------+----------------+-------------+-------------+---------+-------+-----------+------+-------+-----------+------------+---------+------------+----+------------------+
#| MoveIT ID | FleetNumber    | Third party | source_Date | EQ Type | Rate  | JV        | Year | Month | Dayname   | Reg        | TP Code | Weeknumber | id | Transaction_Date |
#+-----------+----------------+-------------+-------------+---------+-------+-----------+------+-------+-----------+------------+---------+------------+----+------------------+
#| 305       | PF423H         |             | 02/01/2019  | Trailer | 23.79 | JV UK     | 2019 |     0 | Wednesday | AS5779     | PF      |          1 |  1 | 2019-01-02       |
#| 1227      | pf576h dehired |             | 02/01/2019  | Hired   | 23.79 | JV UK     | 2019 |     0 | Wednesday | 568890-TIP | PF      |          1 |  2 | 2019-01-02       |
#| 977       | PF726E         |             | 02/01/2019  | Trailer | 23.79 | JV APF    | 2019 |     0 | Wednesday | AS7154     | PF      |          1 |  3 | 2019-01-02       |
#| 804       | PF659E         |             | 02/01/2019  | Trailer | 23.79 | JV FRANCE | 2019 |     0 | Wednesday | AS6870     | PF      |          1 |  4 | 2019-01-02       |
#+-----------+----------------+-------------+-------------+---------+-------+-----------+------+-------+-----------+------------+---------+------------+----+------------------+

from tw_DAO import tw_transactionsDAO as tw
import pandas as pd

df=pd.DataFrame(tw.getAll())
print(df.describe())
print(df.head())

