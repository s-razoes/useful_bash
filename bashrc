alias l='ls -latr'
alias p='ps x|grep [p]ython3'
alias q=exit

#unshort links
function ushort(){
        a=$(echo "$1" | tr '[:upper:]' '[:lower:]')
        if [[ $a != http* ]];then
                u="'https://$1'"
        else
                u="'$1'"
        fi
        curl -k -v -I "'$u'" 2>&1 | grep -i "< location" | cut -d " " -f 3;
}

#empty files
function hollow(){
        cat /dev/null > "$1";
}

#-- ROOT ---
#docker
alias dockH='ContainerId=$(docker stop `docker ps|grep IMAGENAME|cut -d " " -f1`)'
alias dockR='docker start $ContainerId'

#see logs
tail -F `docker inspect --format='{{.LogPath}}' IMAGENAME`

#create docker serving with certificates and redirecting http to https
docker run --mount type=bind,source=/var/www,target=/usr/share/nginx/html,readonly \
--mount type=bind,source=PATH_TO_default.conf_FOLDER,target=/etc/nginx/conf.d,readonly \
--mount type=bind,source=/etc/letsencrypt/live/DOMAIN_NAME/fullfiles,target=/root,readonly \
--name NAMEYOUWISH -p 443:443 -p 80:80 -d nginx ;

#file needs to be in the above folder
default.conf:
server {
listen 443 ssl;
ssl_certificate     /root/fullchain.pem;
ssl_certificate_key /root/privkey.pem;
server_name DOMAIN_NAME;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
server {
    listen 80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}
