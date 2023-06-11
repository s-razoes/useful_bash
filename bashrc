alias l='ls -latrh'
alias p='ps x|grep [p]ython3'

alias alert='telenotify '
alias question='python3 -m telenotify.question_user '
alias q=exit

#mount or unmount if already mounted sshfs drive
alias mt='if [[ $(mount|grep $LOCALPATH|wc -l) -eq 0 ]]; then sshfs -p $PORT $USER@$HOST:$HOSTPATH $LOCALPATH && echo "Mounted..."; else umount $LOCALPATH && echo "UNmounted..."; fi'

#fast vi
alias v='vim -u NONE'

#tmux
sessionName="logs_session"
#start a tmux session or if one detached already exist then open it
function t(){
	mainSessionName="main"
	if [ -n "$TMUX" ]; then
		if [[ "$sessionName" != "$(tmux display-message -p '#S')" ]]; then
			tmux display-panes
			return
		fi
	fi
	if [[ $(tmux ls |grep -v "(attached)"|grep -v "$sessionName"|wc -l) -eq 0 ]]; then
		if [ -n "$TMUX" ]; then
			if [[ $(tmux ls |grep "$mainSessionName"|grep -v "$sessionName"|wc -l) -eq 0 ]]; then
				tmux new -s $mainSessionName -d
			fi
			tmux switch -t $mainSessionName
		else
			tmux new -s $mainSessionName
		fi
	else
		if [ -n "$TMUX" ]; then
			tmux switch -t `tmux ls|grep -v "(attached)"|grep -v "$sessionName"|head -n 1|sed "s/:.*//"`
		else
			tmux attach-session -t `tmux ls|grep -v "(attached)"|grep -v "$sessionName"|head -n 1|sed "s/:.*//"`
		fi
	fi
}

#open tmux with 3 panes for logs
function tl(){
    # if it's in tmux switch to that session
    if [ -n "$TMUX" ]; then
	if [[ "$sessionName" == "$(tmux display-message -p '#S')" ]]; then
		tmux display-panes
		return
	fi
        tmux switch -t $sessionName
    else
        # if session exists already, then switch to it
        if [[ $(tmux ls|grep $sessionName|wc -l) -eq 1 ]]; then
            tmux attach -t $sessionName
        else
	    # These commands can be adjusted to whatever is wanted
            tmux new-session -d -s $sessionName
            tmux send-keys -t $sessionName "echo pane 1, full vertical" Enter
            tmux split-window -h -t $sessionName
            tmux send-keys -t $sessionName "echo pane 2, half vertical" Enter
            tmux split-window -v -p 66 -t $sessionName
            tmux send-keys -t $sessionName "echo pane 2, half vertical" Enter
            tmux attach -t $sessionName
        fi
    fi
}

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

#alternative alert via tcp server
function alert(){
	token="#TCP TOKEN HERE#"
	echo $token"$1"|nc #IP SERVER HERE# #PORT SERVER HERE#
}


#hollow out files without removing permissions
function hollow(){
    cat /dev/null > "$1";
}

#-- ROOT ---
#docker
alias dockH='ContainerId=$(docker stop `docker ps|grep $IMAGENAME|cut -d " " -f1`)'
alias dockR='docker start $ContainerId'

#see logs
tail -F `docker inspect --format='{{.LogPath}}' $IMAGENAME`

#create docker serving with certificates and redirecting http to https
docker run --mount type=bind,source=/var/www,target=/usr/share/nginx/html,readonly \
--mount type=bind,source=PATH_TO_default.conf_FOLDER,target=/etc/nginx/conf.d,readonly \
--mount type=bind,source=/etc/letsencrypt/live/DOMAIN_NAME/fullfiles,target=/root,readonly \
--name $IMAGENAME -p 443:443 -p 80:80 -d nginx ;

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
