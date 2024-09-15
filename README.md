## Setup

You will need the `OPENAI_API_KEY` environment variable.

### Python Environment
You will need to install the python packages in `requirements.txt` to run the python backend.

## Run

Run the development server:

```bash
OPENAI_API_KEY=KEY npm run dev
python server/server.py # Launches python flask backend on port 8080
```
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.



For ad viewer statistics
```bash
python server/dashboard.py # Launches python plotly dashboard
```
Open [http://localhost:8050](http://localhost:8050) with your browser to see the result.


## Add new ads

New ads can be added by:
1. Add an Ad image to the `public/` folder.
2. Run:
```bash
python server/ads.py "Your Ad text here" "ad_img_url" "ad_keyword_1" "ad_keyword_2" "ad_keyword_3" ...
```
Note: img_url can either be a file relative to the public/ dir or a web url to an online image

For example:
```bash
python server/ads.py "Vaccinate your community with Pfizer to protect against Covid-19" "https://logos-world.net/wp-content/uploads/2022/02/Pfizer-Logo.png" covid covid-19 coronavirus
```

