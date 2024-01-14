import React, {useContext, useEffect, useState} from "react";
import "./App.css";
import Navbar from './components/NavbarComponent/Navbar'
import SearchBar from './components/Searchbar'
import DisplayCase from './components/displaycase'
import '@radix-ui/themes/styles.css';
import { Theme } from '@radix-ui/themes';
import axios from 'axios'

export const App = () => {
  const [processedData, setProcessedData] = useState('');
  const [loading, setLoading] = useState(false);

  return (
    <>
    <Theme className="main">
      <Navbar/>
      <SearchBar onSearch={""} processedData={processedData} setProcessedData={setProcessedData} loading={loading} setLoading={setLoading}/>
      <DisplayCase processedData={processedData} setProcessedData={setProcessedData} loading={loading} setLoading={setLoading}/>
    </Theme>
    </>
  );

};

export default App;