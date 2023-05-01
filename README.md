# new route team_id as path param
# by default return csv with all the active drivers for the team



# add arg - List of col headings - 
# construct csv with these columns but always include the id col

# in addition to the col headings, if the arg total race losses is passed, return that
# via pandas calculating win from total

# second endpoint - no path params
# return a csv showing total no. of race wins per team, separated by team and ordered from
# highest to lowest

# bonus points
# test with pandas - the parts with the csv construction
# https://pandas.pydata.org/docs/reference/testing.html

# fastapif1


# Start server:
uvicorn main:app --host localhost --port 8000 --reload



## React Install


```
$ npx create-react-app@5.0.1 frontend
$ cd frontend
```

Next, install a UI component library called Chakra UI:
```
$ npm install @chakra-ui/react@2.0.2
$ npm install @emotion/react@11.9.0 @emotion/styled@11.8.1 emotion-theming@11.0.0

$ cd src
$ mkdir components
$ cd components
$ touch {Header,Todos}.jsx
```


Start your React app from the terminal:
```
$ npm run start
```


##

Run the streamlit browser
```
streamlit run home.py
```