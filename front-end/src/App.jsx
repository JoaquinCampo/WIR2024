import "./styles/App.css";
import React, { useState, useEffect } from "react";
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { zoomies } from 'ldrs';

import { Flex, Text, Divider, Grid, GridItem, Img, Button, Heading,  } from "@chakra-ui/react";
import { CloseIcon } from '@chakra-ui/icons';

import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

import Stat from './components/Stat';
import RedditPost from "./components/RedditPost";
import SuggestCard from "./components/SuggestCard";
// import Scroll from "./components/Scroll";

import candidates from "./politicians.json"
import redditPosts from "./redditPosts.json"
import results from "./results.json"

zoomies.register()
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const logo = "./logoWir.png";
  const [searchValue, setSearchValue] = useState("");
  const [onSubmit, setOnSubmit] = useState(false);
  const [waiting, setWaiting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [progressTarget, setprogressTarget] = useState(0);
  const [nextValue, setNextValue] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");
  // const bg_img = '../istockphoto-1432473911-170667a.webp';
  const bg_img = {
    backgroundImage: `url(${'../istockphoto-1432473911-170667a.webp'})`,
    transform: "scaleX(-1)",
  };

  const handleInputChange = (event) => {
    setSearchValue(event.target.value);
    setErrorMessage("");
  };

  const handlePresetInput = (name) => {
    setprogressTarget(0);
    setSearchValue(name);
    sendRequest(name); // Pass the candidate name directly to sendRequest
  }

  const formSubmit = (event) => {
    event.preventDefault();
    if (searchValue.trim() !== "") {
      sendRequest(searchValue); // Pass the input value to the sendRequest function
    } else {
      setErrorMessage("Por favor ingrese una búsqueda");
    }
  };

  useEffect(() => {
    if (progressTarget > 0) {
      // document.getElementById("scroll-point").scrollIntoView({
      //   behavior: "smooth"
      // });
      var elm = document.querySelector('#progress-indicator');

      const increment = progressTarget / 175;
      const interval = setInterval(() => {
        setProgress((prev) => {
          setNextValue(prev + increment);
          if (nextValue >= progressTarget) {
            clearInterval(interval);
            return progressTarget;
            }
          elm.innerHTML = Math.round(progress * 100) + '%';
          return nextValue;
        });
      }, 1);
      return () => clearInterval(interval);
    }
  }, [progressTarget, nextValue]);

  useEffect(() => {
    window.scrollBy({
      top: 85,
      behavior: "smooth",
    });
  }, [progressTarget])

  async function sendRequest(name) {
    setWaiting(true);
    setProgress(0);

    // Simulate long-running function
    await new Promise(resolve => setTimeout(resolve, 2000));

    switch (name) {
      case "Donald Trump": setprogressTarget(0.5); break;
      case "Joe Biden": setprogressTarget(0.85); break;
      case "Nancy Pelosi": setprogressTarget(0.2); break;
      default: setprogressTarget(parseInt(name));
    }
      setOnSubmit(true);
      setWaiting(false);
  }

  function reset() {      
    window.scrollTo({
    top: 0,
    behavior: "smooth",
  });

    setWaiting(false);
    setOnSubmit(!onSubmit);
  }

  const maxItems = 3;
  redditPosts = redditPosts.slice(0, maxItems);
  return (
    <div className="noise-background" position="fixed" zIndex="-1">
      <Flex className="App" display="inline" position="relative" color="white" height="100%" width="100%">
        <Flex className="top-bg"  bg="#" position="relative" direction="column" min-height="100vh" height="fit-content" alignItems="center" >
          <Flex className="header" position="relative" direction="column" alignItems="center" justifyContent="space-around" width="100%" marginTop="10vh">
            <Flex direction="column" align="center" className={`${onSubmit && !waiting ? "moved" : ""}`} width="100%">
              <Heading className="main-Title" _hover={{cursor:"default"}}> Reputation Analyzer</Heading>
              <Img id="scroll-point" src={logo} className="logo" alt="logoWir" paddingTop="2%" />
            </Flex>

            {onSubmit && !waiting &&
            <Flex className="progress-wrapper" direction="column" transition="opacity 0.2s ease-in-out" height="30vh">
                <CloseIcon color="#a7222c" onClick={reset} position="absolute" right="18%" top="65%"_hover={{color:"red", transform: 'scale(1.3)', transitionDuration: '100ms', WebkitTransform: 'scale(1.3)'}}/>      
                  <progress id="progress-comment" className="progressBar" value={progress} max={1}></progress>
                  <Text id='progress-indicator' _hover={{cursor:"default"}} position="relative" left="25%">0%</Text>
                <Text id="progress-comment" fontSize="2em" position="absolute" bottom="0" bg="none" _hover={{cursor:"default"}}>as</Text>
            </Flex>}

            {waiting &&
            <Flex margin="15%">
              <l-zoomies position="absolute" size="150" stroke="2" bg-opacity="0" speed="0.7" color="cyan"></l-zoomies>
            </Flex>}
          </Flex> 

          <Flex className="idea-container" bgImage={bg_img} marginBottom={1} transition="opacity 0.35s ease-in-out" direction="column" width="80%" marginTop="7vh" display={!onSubmit && !waiting? "" : "none"}>
            <Flex direction="row" alignItems="start" marginTop="2%" justifyContent="center">
              <Flex direction="column" width="30%" marginRight="5%">
                <Divider borderColor="gray.300" ></Divider>
                <Text className="party-name-text" margin="5%" align="center"> Republican Party </Text>

                <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(auto-fit, minmax(20%, 1fr))" gap={10} left="15%">
                  {candidates.filter(candidate => candidate.party === 'Republican Party').map((candidate, index) => (
                    <GridItem className="suggest-card"  overflow="hidden" key={index} _hover={{ cursor: "grab" }} onClick={() => handlePresetInput(candidate.name)}>
                      <SuggestCard  candidateName={candidate.name} candidateImage={candidate.image} />
                    </GridItem>
                  ))}
                </Grid>
              </Flex>
              <Flex  zIndex="1" direction="column" width="30%" marginLeft="5%">
                <Divider borderColor="gray.300" ></Divider>
                <Text className="party-name-text" margin="5%"align="center"> Democratic Party</Text>
                <Grid className="idea-container-content" marginTop="0%" padding="5%" templateColumns="repeat(auto-fit, minmax(20%, 1fr))" gap={10} left="15%">
                  {candidates.filter(candidate => candidate.party === 'Democratic Party').map((candidate, index) => (
                    <GridItem key={index} _hover={{ cursor: "grab" }} onClick={() => handlePresetInput(candidate.name)}>
                      <SuggestCard candidateName={candidate.name} candidateImage={candidate.image} />
                    </GridItem>
                  ))}
                </Grid>
              </Flex>
            </Flex>
          </Flex>
        </Flex>

        <Flex className="lower-bg" bg="#051b33" direction="column" min-height="100vh" height="100vh" alignItems="center" sx={{clipPath: onSubmit ? 'polygon(0% 0%, 50% 4%, 100% 0%, 100% 100%, 0% 110%)' : 'polygon(0 0, 100% 0, 100% 100%, 0 100%)'}} display={onSubmit || waiting ? "flex" : "none"}>
          <Grid className="reddit-posts" position="absolute" width="80%" templateColumns="repeat(auto-fit, minmax(32%, 1fr))" gap={4} borderRadius={20} margin="5%" color="black" opacity={onSubmit && !waiting ? 1 : 0} transition="opacity 0.35s ease-in-out" justifyContent="space-between">
            {redditPosts.map((post, index) => (
              // <Flex className="reddit-post-wrapper" bg="#ff9a00" borderRadius={12}>
              <GridItem>
                <RedditPost title={post.title} subreddit={post.subreddit} date={post.date} content={post.content} upvotes={post.upvotes} _hover={{}} />
              </GridItem>
              // </Flex>
            ))}   
          </Grid>
        </Flex>
      </Flex>
    </div>
  );
}

export default App;
