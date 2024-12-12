#source .env/bin/activate
/home/thiruvalluvar/app/.venv/bin/uvicorn app:app --reload --host=0.0.0.0 --port=9090 &
/home/thiruvalluvar/app/.venv/bin/uvicorn app:app2 --reload --host=0.0.0.0 --port=9100 &
#/home/thiruvalluvar/app/.venv/bin
wait
