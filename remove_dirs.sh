cd ../datacollection

all = ( 1285485_0 1285485_1 1480487_0 1480487_1 1480492_0 1482492_0 1482492_1 1482494_0 1482494_1 1483485_0 1483488_0 1483488_1 1484496_0 1484496_1 1485490_0 1485490_1 1595491_0 1595491_1 1673486_0 1673486_1 1674486_0 1674486_1 2458486_0 2458486_1 2463486_1 2464487_0 2464487_1 2645486_0 2645486_1 2652486_0 2652486_1 2692487_0 2692487_1 2700486_0 2700486_1 2705486_0 2705486_1 2749486_0 2751486_0 2751486_1 2755486_0 2755486_1 )

for i in "${all[@]}"
  do
    cd "solutions_$i" 
    rm -r C 
    rm -r C#
    rm -r java
    rm -r Python
    cd ..
  done