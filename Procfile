web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 application:'create_app()' --preload -b $HOST:$PORT
