# echo "./run.sh <name> <date>"

name="$1"
date="$2"

DATA_PATH=data/$date

python src/rosters.py $DATA_PATH/raw/rosters.csv > $DATA_PATH/rosters.json
python src/standings.py $DATA_PATH/raw/standings.html > $DATA_PATH/standings.json
python src/tournament.py $name $date $DATA_PATH/rosters.json $DATA_PATH/standings.json > $DATA_PATH/tournament.json
python src/tournaments.py data/tournaments.json $DATA_PATH/tournament.json
