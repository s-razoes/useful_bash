#don't forget to change these
SERVER=127.0.0.1
PORT=5003
network=192.168.1.

array=( $( for i in $(seq 254); do ping -c1 -W1 $network$i & done | grep from|sed 's/64 bytes from //'|sed 's/:.*//' ) )
file="known_mac_addresses.txt"
result=($(arp|grep -vi incomplete|awk '{ print $3 }'|tail -n +2))

for i in "${array[@]}"
do
        echo "$i"
done

for i in "${result[@]}"
do
  if grep $i $file; then
    echo "Known $i"
  else
    rst=$(arp|awk '{ print $1, $3 }'|tail -n +2|grep $i)
		url=$(echo "$i"|sed "s/:/%253A/g")
    echo "New in network > $rst https://dnschecker.org/mac-lookup.php?query=$url"|nc $SERVER $PORT
    echo "$i" >> $file					
  fi
done
