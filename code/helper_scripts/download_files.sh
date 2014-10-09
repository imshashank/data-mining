STR="Hello World!"
echo $STR
END=".sgm"
for i in {10..21}
do
   F="http://web.cse.ohio-state.edu/~srini/674/public/reuters/reut2-0$i$END"
   echo $F
   wget $F   
#cat $F >> corpus.pytext
done
