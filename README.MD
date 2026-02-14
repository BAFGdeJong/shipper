<b>How to set up</b> <br>
prerequisites: <br>
cargo, rustc and python installed

`pip install -r requirements.txt` <br>
`maturin develop --release` <br>

Create .env in shipper and set the following variables<br>
WIKI_USERNAME= <br>
WIKI_PASSWORD= <br>


---

<B>How to use</B> <br>
python ship.py -d {starsector data folder} {command}


___

<b>Commands</b> <br>


create - Creates a wikitable table using the requested ship <br>
args <br>
Required: --ship {ship name} <br>
--notes {notes.json in pshipper/data/variant} <br>
--template {template.template in pshipper/templates} <br>
--collapse_after_amount {number} <br>
--write_to_file {file_name} <br>



update - Updates wikitables on starsector.wiki.gg <br>
args <br>
--whitelist {whitelist.json in pshipper/data/variant} <br>
--notes {notes.json in pshipper/data/variant} <br>
--template {template.template in pshipper/templates} <br>

---

<b>Examples</b> <br>
`python ship.py -d D:\Starsector\starsector-core\data\ create -p "Buffalo (A)" -c 3 -w result.txt` <br>
`python ship.py -d D:\Starsector\starsector-core\data\ create -p "Eagle" -c 5` <br>

`python ship.py -d D:\Starsector\starsector-core\data\ update` << Updates all tables on the wiki
