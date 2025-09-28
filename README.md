





Rasbery pi sending weight information to app:

curl -X POST http://127.0.0.1:8000/tools/toolbox/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"weight": 12345}'

  