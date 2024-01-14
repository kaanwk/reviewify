import React, { useEffect, useState } from "react";
import "./Searchbar.css";
import { IoSearchOutline } from "react-icons/io5";
import axios from "axios";

const SearchBar = (props, { onSearch }) => {

  const [restaurant, setInput1] = useState('');
  const [postal, setInput2] = useState('');

  const sendDataToFlask = async () => {
    props.setLoading(true);
    const apiUrl = 'http://localhost:5000/flask/process_data';

    const requestData = {
      restaurant: restaurant,
      postal: postal,
    };

    try {
      const response = await axios.post(apiUrl, requestData);
      props.setProcessedData(response.data.message);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      props.setLoading(false)
    }
  };

  if (props.loading === true) {
    return (
      <>
      <span></span>
      </>
    );
  }

  
  return (
    <>
      <div class="new-search">
        <input
          type="text"
          value={restaurant}
          onChange={(e) => setInput1(e.target.value)}
          placeholder="Business Name"
          class="searchInput"
        />
        <input
          type="text"
          value={postal}
          onChange={(e) => setInput2(e.target.value)}
          placeholder="Postal code"
          class="searchInput"
        />
      <button onClick={sendDataToFlask} id="searchButton">Search</button>
    </div>
    </>
  );
};

export default SearchBar;
