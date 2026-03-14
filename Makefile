.PHONY: start stop restart tunnel dev logs status

start:
	@echo "Starting Pantry Assistant..."
	@nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 & echo $$! > server.pid
	@sleep 1
	@echo "Server running at http://localhost:8000 (PID $$(cat server.pid))"

stop:
	@if [ -f server.pid ]; then \
		kill $$(cat server.pid) 2>/dev/null && echo "Server stopped." || echo "Server was not running."; \
		rm -f server.pid; \
	else \
		echo "No server.pid found. Trying pkill..."; \
		pkill -f "uvicorn app.main" && echo "Server stopped." || echo "Server was not running."; \
	fi

restart: stop start

dev: start
	@echo "Opening HTTPS tunnel (Ctrl+C to stop tunnel — run 'make stop' to stop server)..."
	ngrok http 8000

tunnel:
	@echo "Opening HTTPS tunnel (Ctrl+C to close)..."
	ngrok http 8000

logs:
	@tail -f server.log

status:
	@pgrep -a -f "uvicorn app.main" && echo "Server is running." || echo "Server is not running."
