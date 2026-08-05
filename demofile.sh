
mkdir templates 
python3 scaffold.py gemplace lat lon name description
python3 scaffold.py language name
python3 scaffold.py job name
python3 scaffold.py userhasjob job_id:references user_id:references
python3 scaffold.py programming_script lat lon title description
python3 scaffold.py user username email password phone country_id:references
python3 scaffold.py post title description user_id:references language_id:references
python3 scaffold.py musicalscore time_signature key_signature title content user_id:references
python3 scaffold.py sharewithgeniusmusicalscore musicalscore_id:references description job_id:references gemplace_id:references
python3 scaffold.py calluponaiprogrammingscript programming_script_id:references description job_id:references gemplace_id:references
python3 scaffold.py sharepost user_id:references post_id:references description job_id:references gemplace_id:references
