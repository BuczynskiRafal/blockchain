import React, {useState} from "react";


function App() {
  const [userQuery, setUserQuery]  useState('');
  const updateUserQuery = event => {
    console.log('userQuery', userQuery);
    setUserQuery(event.target.value);
  }

  const searchQuery = () => {}

  return (
    <div className="App">
      <input value={userQuery} onChange={updateUserQuery} />

    </div>
  );
}

export default App;
