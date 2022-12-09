# ![Flight Tracker Simulator](https://imgur.com/s13uQen.gif)
# Flight Tracker Simulator
<table>
<tr>
<td>
  A webapp built using streamlit. Currently this app is only a simulation but it can be easily adapted to generate the realtime location of any commercial flight utilizing its on board instrument data. All data in the application is accurate aside from the actual simulated flight. The distance between two airports, the average flight time and the ability to detect which airports contain direct flights to each other are discussed below.
</td>
</tr>
</table>


## Data
The data used in this application was sourced from historical flight data freely available online. The distance between two geographic locations is generated by utilzing the haversine formula. The average flight time between two airports was generated by averaging thousands of historical flights from one airport to another.





## Mobile support
The WebApp is compatible with devices of all sizes and all OS's, and consistent improvements are being made.


## [Usage](https://joshjetson-flight-tracker-strmlt-fts-gb1qxl.streamlit.app/) 
- Click on Usage ^^ to use the deployed app!
### Development
Want to contribute? Great!

To fix a bug or enhance an existing module, follow these steps:

- Fork the repo
- Create a new branch (`git checkout -b improve-feature`)
- Make the appropriate changes in the files
- Add changes to reflect the changes made
- Commit your changes (`git commit -am 'Improve feature'`)
- Push to the branch (`git push origin improve-feature`)
- Create a Pull Request 

### Bug / Feature Request

If you find a bug (the website couldn't handle the query and / or gave undesired results), kindly open an issue.


## Built with 

- [Streamlit](https://streamlit.io/) - An application framework which caters to rapid web app development.
- [Python](https://www.python.org/)
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [Pydeck](https://pydeck.gl/) - A High-scale spatial rendering engine for data visualization in Python, powered by [deck.gl](https://deck.gl/#/).


## To-do
- Utilize real time data generated from on-board flight instruments




