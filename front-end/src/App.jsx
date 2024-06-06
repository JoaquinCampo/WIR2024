import "./styles/App.css";
import React, { useState, useEffect } from "react";
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { zoomies } from 'ldrs';

import { Flex, Box, Text, Divider, Grid, GridItem, Img, FormControl, FormErrorMessage, FormErrorIcon, Input } from "@chakra-ui/react";
import { ChakraProvider } from '@chakra-ui/react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

import Stat from './components/Stat';
import RedditPost from "./components/RedditPost";
import SuggestCard from "./components/SuggestCard";
// import Scroll from "./components/Scroll";

import candidates from "./politicians.json"

zoomies.register()
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);


let aux = false;


function App() {
  const logo = "./logoWir.png";
  const [searchValue, setSearchValue] = useState("");
  const [onSubmit, setOnSubmit] = React.useState(false);
  const [waiting, setWaiting] = React.useState(false);
  const [progress, setProgress] = useState(0);
  const [targetProgress, setTargetProgress] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");

  const handleInputChange = (event) => {
    setSearchValue(event.target.value);
    setErrorMessage("");
  };

  const handlePresetInput = (name) => {
    console.log(name + "2")
    setSearchValue(name);
    sendRequest(searchValue);
  }

  const formSubmit = (event) => {
    event.preventDefault();
    if(searchValue.trim() != ""){
      console.log("if");
      sendRequest(searchValue); // Pass the input value to the sendRequest function
    }else{
      console.log("else");
      setErrorMessage("Por favor ingrese una búsqueda");
    }
  };
  
  useEffect(() => {
    if (onSubmit && !waiting) {
      const increment = (progress) / (70);
      const interval = setInterval(() => {
        setProgress((prev) => {
          const nextValue = prev + increment;
          if (nextValue >= progress) {
            clearInterval(interval);
            return progress;
          }
          return nextValue;
        });
      });

      return () => clearInterval(interval);
    }
  });

  function sendRequest(e) {
    setWaiting(true);
    console.log(searchValue);
    switch(searchValue){
      case "Donald Trump": setProgress(0.5); break;
      case "Joe Biden" : setProgress(0.85); break;
      case "Nancy Pelosi": setProgress(0.2); break;
      default: setProgress(parseInt(e));
    }
    // setProgress(0.9);
    setTimeout(() => {
      setOnSubmit(true);
      setWaiting(false);
    }, 3000);
  }



  return (
    <ChakraProvider>
      <Flex className="App"  bg="#282c34"  width="100%">
          <h1 className={`main-Title ${onSubmit && !waiting ? "moved" : ""}`}>Reputation Analyzer</h1>
          
          <Img src={logo} className={`logo ${onSubmit && !waiting ? "moved" : ""}`} alt="logoWir"/>
          {/* <Scroll /> */}

          <Flex className= {`search-container ${onSubmit || waiting ? "disappear" : ""}`} >
            <form className="form" onSubmit={formSubmit} display="flex" alignItems="center"
            justifyContent="center">
              {/* <FormControl> */}
                <input
                border={0}

                  name="request"
                  className="Barra-busqueda"
                  type="search"
                  placeholder="Ingrese su búsqueda" 
                  autoComplete="off"
                  onChange={handleInputChange}
                  />
                  <button className="submit-button" type="search"> <FontAwesomeIcon icon={faSearch} color="#76c7c0"/> </button>
                  {/* </FormControl> */}
                {/* {errorMessage && <FormErrorIcon/>} */}
                {errorMessage && <FormErrorMessage>{errorMessage}</FormErrorMessage>}
            </form>
          </Flex>

          {onSubmit && !waiting && <Flex className="progress-wrapper" opacity={onSubmit && !waiting ? 1 : 0}
          transition="opacity 0.2s ease-in-out" >
            <progress className="progressBar" value={progress} max = {1} />
          </Flex>}

          {waiting &&<l-zoomies
            size="150"
            stroke="2"
            bg-opacity="0"
            speed="0.7" 
            color="cyan" 
            ></l-zoomies>}
        {/* <Flex className="idea-container-background" bg="white" width="80%"> */}
          <Flex direction="column" className="idea-container" bg="#282c34" paddingLeft="5%" paddingTop="5%" width="80%" marginTop="15%"borderRadius="10px" opacity={!onSubmit || waiting ? 1 : 0}>
            <Divider borderColor="gray.300" ></Divider>
            <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(auto-fit, minmax(12%, 1fr))" gap={10} left="15%">
              {candidates.map((candidate, index) => (
                <GridItem _hover={{cursor:"grab"}} onClick={() => handlePresetInput(candidate.name.toString())}>
                  <SuggestCard  key={index} candidateName={candidate.name} candidateImage={candidate.image}/>
                </GridItem>
              ))}
            </Grid>
          </Flex>
        {/* </Flex> */}

          <Flex className="reddit-posts"  width="100%" borderRadius={20} margin="15%" color="black" opacity={onSubmit && !waiting ? 1 : 0}
            transition="opacity 0.35s ease-in-out" justifyContent="space-between" bg="none">
              {/* <Flex className="reddit-post-wrapper"  bg="#ff9a00" borderRadius={12}> */}
                <RedditPost title="Question: What makes a good Security Engineer?" subreddit="r/politics" date="2 d ago" content="In your opinion what makes or breaks a good Security Engineer in the AppSec or IaC world?"  upvotes="5"/>
              {/* </Flex> */}
              {/* <Flex className="reddit-post-wrapper"  bg="#ff9a00" borderRadius={12}> */}
                <RedditPost title="Question: What makes a good Security Engineer?" subreddit="r/politics" date="2 d ago" content="In your opinion what makes or breaks a good Security Engineer in the AppSec or IaC world?" upvotes="5"/>
              {/* </Flex> */}
              {/* <Flex className="reddit-post-wrapper"  bg="#ff9a00" borderRadius={12}> */}
                <RedditPost title="Question: What makes a good Security Engineer?" subreddit="r/politics" date="2 d ago" content="In your opinion what makes or breaks a good Security Engineer in the AppSec or IaC world?" upvotes="5"/>
              {/* </Flex> */}
          </Flex>
          <Flex direction="column" bg="green" position="absolute" className="statistics" width="100%" height="auto" opacity={onSubmit && !waiting ? 1 : 0}   justifyContent="space-between" alignItems="center">
            <div className="test"></div>
            <Stat></Stat>
            <Stat></Stat>
          </Flex>

        </Flex>
    </ChakraProvider>
  );
}

export default App;

