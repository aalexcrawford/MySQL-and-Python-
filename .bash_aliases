alias start_flask="nohup uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app &"
alias stop_flask="sudo pkill -9 uwsgi"
alias debug_flask="uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app&"
alias mysql_login="mysql -u aalex -h incognito-db.cldmcuhzf49p.us-east-2.rds.amazonaws.com -p"

function restart_flask() {
	stop_flask
	start_flask
}
