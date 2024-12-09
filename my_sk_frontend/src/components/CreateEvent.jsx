import { useState } from 'react';
import { DefaultInput, DefaultTextArea } from './Input.jsx';
import axios from 'axios';

axios.defaults.baseURL = 'http://0.0.0.0:8000';

const EventInfo = ({
  submitUrl,
  requestMethod,
  eventName,
  date,
  startTime,
  endTime,
  description,
  tags
}) => {
  const [formData, setFormData] = useState({
    eventName: eventName ? eventName : '',
    date: date ? date : '',
    startTime: startTime ? startTime : '',
    endTime: endTime ? endTime : '',
    description: description ? description : '',
    tags: tags ? tags : []
  });

  const [validationResult, setValidationResult] = useState({
    tags: ''
  });

  const [success, setSuccess] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem('authToken');
    const requestBody = {
      name: formData.eventName,
      start: new Date(`${formData.date} ${formData.startTime}`).toISOString(),
      end: new Date(`${formData.date} ${formData.endTime}`).toISOString(),
      description: formData.description === '' ? formData.description : null,
      tags: formData.tags.length === 0 ? formData.tags : null
    };
    const requestHeaders = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    };

    axios
      .request({
        method: requestMethod,
        url: submitUrl,
        data: requestBody,
        headers: requestHeaders
      })
      .then(() => {
        setSuccess('Successfully created event!');
        setValidationResult((currentState) => {
          return { ...currentState, creatiion: '' };
        });
      })
      .catch((error) => {
        let errorMessage = 'An unexpected error occurred!';
        const rejected_response = error.response;

        if (rejected_response) {
          errorMessage = rejected_response.data.detail;
        }
        setValidationResult((currentState) => {
          return { ...currentState, creatiion: errorMessage };
        });
        setSuccess('');
      });
  };

  return (
    <div style={{ flexDirection: 'column', display: 'flex', alignItems: 'flex-end' }}>
      <form onSubmit={handleSubmit}>
        <DefaultInput
          type="text"
          name="eventName"
          label="Event name"
          ExternalState={formData}
          setExternalState={setFormData}
          pattern="[a-zA-Z0-9_.\-\s]+"
          required={true}
        />
        <DefaultInput
          type="date"
          name="date"
          label="Start"
          ExternalState={formData}
          setExternalState={setFormData}
          required={true}
        />
        <DefaultInput
          type="time"
          name="startTime"
          label="Start time"
          ExternalState={formData}
          setExternalState={setFormData}
          required={true}
        />
        <DefaultInput
          type="time"
          name="endTime"
          label="End time"
          ExternalState={formData}
          setExternalState={setFormData}
          min={formData.startTime}
          required={true}
        />
        <DefaultTextArea
          type="text"
          name="description"
          label="Event's description"
          ExternalState={formData}
          setExternalState={setFormData}
        />
        <button type="submit">Create Event</button>
        {validationResult.creatiion === '' ? null : (
          <p style={{ color: 'red' }}>{validationResult.creatiion}</p>
        )}
        {success == '' ? null : <p style={{ color: 'green' }}>{success}</p>}
      </form>
    </div>
  );
};

const CreateEvent = ({ ...props }) => {
  return (
    <div>
      <h2>Create Event</h2>
      <EventInfo submitUrl="/calendar" requestMethod="post" {...props} />
    </div>
  );
};

export { CreateEvent, EventInfo };
