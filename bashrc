alias l='ls -latr'
alias p='ps x|grep [p]ython3'
alias q=exit

#unshort links
function ushort(){
        a=$(echo "$1" | tr '[:upper:]' '[:lower:]')
        if [[ $a != http* ]];then
                u='https://'$1
        else
                u=$1
        fi
        curl -k -v -I "$u" 2>&1 | grep -i "< location" | cut -d " " -f 3;
}

#empty files
function hollow(){ cat /dev/null > "$1"; }
