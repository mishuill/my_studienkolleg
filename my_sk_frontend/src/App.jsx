import { useState, useEffect } from 'react';
import axios from 'axios';

import EventCard from './components/EventCard.jsx';
import { CreateEvent } from './components/CreateEvent.jsx';
import { Register, Login } from './components/AuthenticationPanel.jsx';

axios.defaults.baseURL = 'http://0.0.0.0:8000';

const App = () => {
  const submitUrl = '/calendar/list';

  const [Events, setEvents] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const requestConfig = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    };
    axios
      .get(submitUrl, requestConfig)
      .then((response) => {
        const documents = response.data.documents;
        setEvents(documents);
      })
      .catch((error) => {
        if (error.request.status == 403) console.log('Token Expired');
      });
  });

  return (
    <>
      <div
        style={{
          flexDirection: 'row',
          display: 'flex',
          justifyContent: 'space-around',
          alignItems: 'center',
          gap: '10px'
        }}>
        <Login />
        <Register />
      </div>

      <div
        style={{
          flexDirection: 'row',
          display: 'flex',
          justifyContent: 'space-around',
          alignItems: 'center'
        }}>
        <div
          style={{
            flexDirection: 'column',
            display: 'flex',
            justifyContent: 'space-around',
            alignItems: 'center'
          }}>
          {Events.sort((a, b) => {
            return new Date(b.start) - new Date(a.start);
          })
            .slice(0, 5)
            .map((event, index) => (
              <EventCard key={index} event={event} />
            ))}
        </div>
        <CreateEvent />
      </div>
    </>
  );
};

export default App;
