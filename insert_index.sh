#gets a json spread over multiple lines and inserts " index " properties before each line
filename="tmp"
filename2="final.json"

truncate -s 0 $filename2

j=1
while read line;
do
	echo "{ \"index\" : { \"_index\" : \"engine\", \"_type\" : \"type1\", \"_id\" : \"$j\" } }" >> $filename2;
	echo $line >> $filename2 ;
	((j++))
done < $filename
