const EventCard = ({ event }) => {
  return (
    <div
      style={{
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '16px',
        margin: '16px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
      }}>
      <h2 style={{ margin: '0 0 8px' }}>{event.name}</h2>
      <p style={{ color: '#555', margin: '0 0 16px' }}>
        <strong>Start:</strong> {new Date(event.start).toLocaleDateString()} at (
        {new Date(event.start).toLocaleTimeString()})
      </p>
      <p style={{ color: '#555', margin: '0 0 16px' }}>
        <strong>End:</strong> {new Date(event.end).toLocaleDateString()} at (
        {new Date(event.end).toLocaleTimeString()})
      </p>
      {event.user_id ? (
        <p style={{ margin: '0 0 16px', color: '#666' }}>
          <strong>Organizer:</strong>
          {event.user_id}
        </p>
      ) : null}
      {event.description ? (
        <div>
          <h3 style={{ margin: '0 0 8px' }}>Event Description</h3>
          <p style={{ margin: '0 0 16px', color: '#666' }}>{event.description}</p>
        </div>
      ) : null}
    </div>
  );
};

export default EventCard;
