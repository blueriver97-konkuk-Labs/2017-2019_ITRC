#source ../bin/activate
rm moocacha/migrations/000*
rm db.sqlite3

rm media/video/*
rm media/audio/*
rm media/script/*
rm media/thumbnail/*
rm media/aiml/*

python3 manage.py makemigrations
python3 manage.py migrate
echo 'yes' | python3 manage.py collectstatic 

#nohup python3 manage.py runserver 0.0.0.0:8000 &
python3 manage.py runserver 0.0.0.0:8000
